# Star Citizen Helper AI Bot

Welcome to the Star Citizen Helper AI Bot! This bot is designed to assist players of the game Star Citizen by providing detailed, accurate, and helpful information. Leveraging the power of advanced AI models and various APIs, this bot aims to enhance your in-game experience.

## Features

- **Role Assignment**: Users can react to a message to get assigned specific roles.
- **Joke Command**: Provides a random joke to lighten up the mood.
- **AI Query Command**: Allows users to query an AI assistant for detailed information about Star Citizen.

## AI Integration

The bot uses advanced AI models and LangChain to generate responses and perform complex queries, returning comprehensive answers to enhance the player’s experience in the game Star Citizen.

### LangChain Components

- **ChatOpenAI**: Utilizes AI models for generating responses.
- **APIChain**: Facilitates interactions with external APIs
- **ConstitutionalChain**: Ensures that the AI responses adhere to specific principles and guidelines, making the bot's output reliable and relevant.

## APIs Used

### Star Citizen Fandom Wiki API

This API allows the bot to fetch detailed game data such as player information, ship details, and more. The bot can perform various queries to retrieve and present this data in a user-friendly format.

### Reddit API

The bot also integrates with Reddit to fetch discussions and posts from the Star Citizen subreddit. This allows the bot to provide community-driven insights and updates.

## Commands

- **/roles**: Creates a role assignment message. Users can react with specific emojis to get assigned roles like Scavenger, Pirate, Bounty Hunter, or Flexible.
- **/joke**: Tells a random joke.
- **/ai**: Queries the AI for detailed Star Citizen information.

## How to Use

1. **Setting Up**: Ensure you have the necessary environment variables set up in a `.env` file. This includes the bot token, channel ID, OpenAI API key, and Reddit API credentials.
2. **Running the Bot**: Execute the bot script to get it running on your Discord server. Users can interact with the bot using the defined commands.
3. **Role Assignment**: Users can react to the role assignment message to get assigned specific roles automatically.
4. **Querying the AI**: Use the `/ai` command followed by your query to get detailed information from the AI.

## To run this program, you need to install the following packages:

- `discord.py`: For interacting with the Discord API.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `aiohttp`: For making asynchronous HTTP requests.
- `praw`: For interacting with the Reddit API.
- `openai`: For accessing OpenAI's GPT models.
- `langchain`: For leveraging LangChain's capabilities in processing AI queries.

You can install these dependencies using pip:

```sh
pip install discord.py python-dotenv aiohttp praw openai langchain