from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, APIChain
from langchain.chains.constitutional_ai.base import ConstitutionalChain
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import aiohttp
import praw
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

# Set the model name for our LLMs
OPENAI_MODEL = "gpt-4-turbo"
# Store the API key in a variable
OPENAI_API_KEY = os.getenv("OPENAI_KEY")

# Initialize Reddit API client
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Initialize the model.
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL, temperature=0.0)

spec_str = """The Star Citizen Fandom Wiki provides an API to search for information about the game.

WARNING: This API is under active development and may change in the future.

Overview & Features
The Star Citizen Fandom Wiki API is one of the most convenient and complete ways to retrieve game data. The API:

- Supports queries to retrieve specific information about players, ships, and other game data.
- Allows fetching of multiple items in a single request.
- Returns detailed information including snippets, timestamps, size, and word count of the retrieved content.

Endpoint
The endpoint for this API is:
https://starcitizen.fandom.com/api.php

Examples
The URL format for the API is simple. Use the base URL and add the appropriate parameters. Examples:

https://starcitizen.fandom.com/api.php?action=query&format=json&list=search&srsearch=Star%20Citizen
https://starcitizen.fandom.com/api.php?action=query&format=json&list=search&srsearch=Aurora&srlimit=5
https://starcitizen.fandom.com/api.php?action=query&format=json&list=search&srsearch=Chris%20Roberts&srprop=snippet|timestamp|size|wordcount

URL Parameters
Parameter    Description
action       The action to be performed. For search queries, use 'query'.
format       The format of the response. Use 'json' for JSON format.
list         The type of list to retrieve. For search queries, use 'search'.
srsearch     The search query string. This is where you input your search terms.
srlimit      The number of search results to return. Default is 10, with a maximum of 500.
srprop       The properties to return for each search result. Options include 'snippet', 'timestamp', 'size', and 'wordcount'.

Fetch Library Information
Fetch is a library for getting and caching API requests. It also includes special support for getting and processing system messages.

Usage
Importing
To import and use the Fetch library inside your script, use the following.

mw.hook('dev.fetch').add(function (fetch) {
    // your code here
});
importArticle({
    type: 'script',
    article: 'u:dev:MediaWiki:Fetch.js'
});

Methods
The library exports the window.dev.fetch method, which accepts one parameter. This parameter may be formatted in three ways.

If the parameter is a string, the library will get that message and return it as a string. If the string contains multiple messages separated by | (e.g. block|userrights), it will get each of the messages and return them as a function. Invoking the function without a parameter will return an object of all the messages, while supplying a parameter returns the value of that key in the object. The key can be either the message name or its index.
If the parameter is an array, the library will get the specified messages and return them as an invokable function (see above).
If the parameter is an object, it can have the following properties, all of which are optional.
Name    Description    Default    Type
lang    The language to get the system messages in. Use only with messages.    wgUserLanguage    string
messages    The system messages to get.    N/A    string or array
process    Processing that should be applied to the data before it gets returned.    N/A    function
request    The API request and callback to execute.    N/A    function
time    The time, in milliseconds, that the request should be cached for.    One day    number
noCache    Whether the request should be cached. Not recommended except for personal debugging purposes.    false    boolean
After completing the API request or retrieving the cache, the library returns a promise.

Examples
This gets a single message.
mw.hook('dev.fetch').add(function (fetch) {
    fetch('block').then(function (msg) {
        $('.wds-list').append('<li>' + msg + '</li>');
    });
});
This gets multiple messages.
mw.hook('dev.fetch').add(function (fetch) {
    fetch('block|userrights').then(function (msg) {
        $('.wds-list').append('<li>' + msg()[0] + msg('userrights') + '</li>');
    });
});
This gets multiple messages in German with a two day delay.
mw.hook('dev.fetch').add(function (fetch) {
    fetch({
        lang: 'de',
        messages: ['block', 'userrights'],
        time: 2 * 24 * 60 * 60 * 1000
    }).then(function (msg) {
        $('.wds-list').append('<li>' + msg('block') + msg()[1] + '</li>');
    });
});
This executes and caches an API request. Note that the request function accepts two parameters, which should be used to resolve the library's promise.
mw.hook('dev.fetch').add(function (fetch) {
    fetch({
        request: function (resolve, reject) {
            new mw.Api().get({
                action: 'query',
                titles: 'MediaWiki:ImportJS'
            }).done(function (d) {
                if (d.error) {
                    reject(d.error.code);
                } else {
                    resolve(d.query.pages);
                }
            }).fail(function () {
                reject();
            });
        },
        name: 'PageExists'
    }).then(function (d) {
        if (!d[-1]) {
            console.log('MediaWiki:ImportJS exists!');
        }
    });
});

Cache
Each cache, by default, lasts for one day, after which it is updated. The entire Fetch cache is also regularly cleared approximately every 100 page loads. To bypass this cache, simply add ?debug=1 to the URL, which will delete every Fetch item and re-run every API request. Alternately, use the keyboard commands Ctrl + F5 or Ctrl + ⇧ Shift + R, which will do the same thing and reload the page. To bypass cache for just one script, simply set the noCache option to true.

Dependents
List of dependents using this library

Changelog
Version    Date    Description    Author
"""

# Initialize the model.
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL, temperature=0.0)

api_chain = APIChain.from_llm_and_api_docs(
    llm,
    api_docs=spec_str,
    limit_to_domains=["https://starcitizen.fandom.com/api.php?"],
    verbose=True,
)

async def query_star_citizen_api(query: str, limit: int = 1):
    search_url = f"https://starcitizen.fandom.com/api.php?action=query&format=json&list=search&srsearch={query}&srlimit={limit}&srprop=snippet|timestamp|size|wordcount"
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            search_response = await response.json()
    
    if 'query' not in search_response or 'search' not in search_response['query'] or not search_response['query']['search']:
        return "No results found."
    
    articles = search_response['query']['search']
    article_data = []

    for article in articles:
        pageid = article['pageid']
        
        # Step 2: Retrieve detailed content using the pageid
        content_url = f"https://starcitizen.fandom.com/api.php?action=query&format=json&prop=revisions&pageids={pageid}&rvprop=content"
        async with aiohttp.ClientSession() as session:
            async with session.get(content_url) as response:
                content_response = await response.json()
        
        if 'query' not in content_response or 'pages' not in content_response['query'] or str(pageid) not in content_response['query']['pages']:
            article_content = "Failed to retrieve detailed content."
        else:
            page_data = content_response['query']['pages'][str(pageid)]
            if 'revisions' not in page_data or not page_data['revisions']:
                article_content = "No content available for the page."
            else:
                page_content = page_data['revisions'][0]['*']
                plain_text_content = page_content.replace("'''", "").replace("''", "").replace("[[", "").replace("]]", "").replace("=", "")
                article_content = plain_text_content
        
        article_info = {
            "Title": article['title'],
            "PageID": article['pageid'],
            "Content": article_content,
            "Snippet": article['snippet'],
            "Timestamp": article['timestamp'],
            "Size": article['size'],
            "Wordcount": article['wordcount']
        }
        article_data.append(article_info)

    return article_data

async def query_reddit_api(subreddit: str, query: str, limit: int = 1):
    # Use praw in a blocking way since asyncpraw is recommended for async environments.
    # Ensure your bot can handle this properly.
    search_results = reddit.subreddit(subreddit).search(query, limit=limit)
    
    post_data = []
    for post in search_results:
        post_info = {
            "Title": post.title,
            "PostID": post.id,
            "Content": post.selftext,
            "Snippet": post.selftext[:200] + '...' if len(post.selftext) > 200 else post.selftext,
            "Timestamp": post.created_utc,
            "Score": post.score,
            "Comments": post.num_comments
        }
        post_data.append(post_info)
    
    return post_data

async def combined_query(query: str, subreddit: str):
    star_citizen_data = await query_star_citizen_api(query)
    reddit_data = await query_reddit_api(subreddit, query)
    
    combined_data = {
        "star_citizen": star_citizen_data,
        "reddit": reddit_data
    }
    
    return combined_data

chat_llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL, temperature=0.2)

prompt_template = PromptTemplate(
    template="""You are the Star Citizen Helper AI, a highly advanced AI assistant designed to help players navigate the vast universe of Star Citizen. 
    Your primary goal is to provide detailed, accurate, and helpful information to enhance the player's experience. Assume all questions are referring to
    in-game information. Answer the following query as concisely as possible using the provided API data. Search for the top 5-10 results.
    
    API Data: {api_data}
    Query: {query}
    """,
    input_variables=["api_data", "query"]
)

# Create a chat chain for creating the recipes.
chat_chain = LLMChain(llm=chat_llm, prompt=prompt_template)

principle = ConstitutionalPrinciple(
    name='Outside sources',
    critique_request = 'The model should not mention outside sources, such as the API data',
    revision_request = 'Modify the response to not mention outside sources, such as the API data, DO NOT MENTION API DATA'
)

principle_2 = ConstitutionalPrinciple(
    name='suggest',
    critique_request = 'If the player requests something such as a build for a ship, offer suggestions for specific components',
    revision_request = 'Modify the response to include specific suggested components'
)

principle_3 = ConstitutionalPrinciple(
    name='Missing Data',
    critique_request = 'Even if there is no relevant information in the provided API data, you still need to answer the question.',
    revision_request = 'Modify the response to include a confident response to the query that does not mention API data'
)



constitutional_chain = ConstitutionalChain.from_llm(
    chain=chat_chain,
    constitutional_principles = [principle, principle_2, principle_3],
    llm=chat_llm,
    verbose=True
    )

executor = ThreadPoolExecutor(max_workers=4)

async def query_ai(query: str):
    subreddit_name = 'starcitizen'
    api_result = await combined_query(query, subreddit_name)
    query_input = {'query': query, 'api_data': api_result}
    loop = asyncio.get_event_loop()
    final_result = await loop.run_in_executor(executor, constitutional_chain.invoke, query_input)
    return final_result['output']
