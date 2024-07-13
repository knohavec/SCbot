import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import random

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
channel_id = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True  # Ensure members intent is enabled

bot = commands.Bot(command_prefix='!', intents=intents)

role_message_id = None  # Will be set when /roles command is used
emoji_to_role = {
    '🗑️': 'Scavenger',
    '🏴‍☠️': 'Pirate',
    '🎯': 'Bounty Hunter',
    '🌀': 'Flexible',  # or '🔄' for Adaptable
}

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
    "Why don’t some couples go to the gym? Because some relationships don’t work out.",
    "I would avoid the sushi if I was you. It’s a little fishy.",
    "Want to hear a joke about construction? I’m still working on it.",
    "Why don’t you ever see elephants hiding in trees? Because they’re so good at it."
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_raw_reaction_add(payload):
    print(f'Reaction added: {payload.emoji} by user {payload.user_id}')
    if payload.message_id == role_message_id:
        guild = bot.get_guild(payload.guild_id)
        if guild:
            role_name = emoji_to_role.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member is None:
                        try:
                            member = await guild.fetch_member(payload.user_id)
                            print(f'Fetched member {member.name} from guild {guild.name}')
                        except discord.NotFound:
                            print(f'Member with ID {payload.user_id} not found in guild {guild.name}')
                            return
                    try:
                        await member.add_roles(role)
                        print(f'Added role {role_name} to user {member.name}')
                    except Exception as e:
                        print(f'Failed to add role {role_name} to user {member.name}: {e}')
                else:
                    print(f'Role {role_name} not found in guild {guild.name}')
            else:
                print(f'No role found for emoji {payload.emoji}')
        else:
            print(f'Guild not found for ID {payload.guild_id}')

@bot.event
async def on_raw_reaction_remove(payload):
    print(f'Reaction removed: {payload.emoji} by user {payload.user_id}')
    if payload.message_id == role_message_id:
        guild = bot.get_guild(payload.guild_id)
        if guild:
            role_name = emoji_to_role.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member is None:
                        try:
                            member = await guild.fetch_member(payload.user_id)
                            print(f'Fetched member {member.name} from guild {guild.name}')
                        except discord.NotFound:
                            print(f'Member with ID {payload.user_id} not found in guild {guild.name}')
                            return
                    try:
                        await member.remove_roles(role)
                        print(f'Removed role {role_name} from user {member.name}')
                    except Exception as e:
                        print(f'Failed to remove role {role_name} from user {member.name}: {e}')
                else:
                    print(f'Role {role_name} not found in guild {guild.name}')
            else:
                print(f'No role found for emoji {payload.emoji}')
        else:
            print(f'Guild not found for ID {payload.guild_id}')

@bot.tree.command(name="roles", description="Create a role assignment message")
async def roles(interaction: discord.Interaction):
    global role_message_id
    message_content = (
        "React to this message to get a role:\n"
        "🗑️ for Scavenger\n"
        "🏴‍☠️ for Pirate\n"
        "🎯 for Bounty Hunter\n"
        "🌀 for Flexible (or 🔄 for Adaptable)"
    )
    message = await interaction.channel.send(message_content)
    role_message_id = message.id
    for emoji in emoji_to_role.keys():
        await message.add_reaction(emoji)
    await interaction.response.send_message("Role assignment message created!", ephemeral=True)

@bot.tree.command(name="joke", description="Tells a joke")
async def joke(interaction: discord.Interaction):
    joke = random.choice(jokes)
    await interaction.response.send_message(joke, ephemeral=True)

bot.run(BOT_TOKEN)
