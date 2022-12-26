import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is online")

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    
    if "http" in message.content and len(message.content) > 4:
        await message.delete()
        await message.channel.send(f"{message.author.mention} you can't send links here.")

with open("secrets.json", "r") as f:
    data = json.load(f)
TOKEN = data['TOKEN']

bot.run(TOKEN)