import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name='ban', description='bans a user')
async def ban(interaction : discord.Interaction, user : discord.Member, delete_message_days : int = None, reason : str = None):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(embed=discord.Embed(description="You don't have required permissions.", color=0xff5050))

    if delete_message_days > 7 or delete_message_days < 0:
        await interaction.response.send_message(embed=discord.Embed(description='Invalid amount of days.', color=0xff5050))

    await user.ban(reason=reason, delete_message_seconds=delete_message_days * 86400)
    await interaction.response.send_message(embed=discord.Embed(description=f"Banned {user} for {reason}", color=0x50ff50), ephemeral=True)

@bot.tree.command(name='purge', description='deletes a specific amount of messages')
async def purge(interaction : discord.Interaction, amount : int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(embed=discord.Embed(description="You don't have required permissions.", color=0xff5050))

    await interaction.response.send_message(embed=discord.Embed(description=f'Deleting {amount} messages.', color=0xff5050))
    await interaction.delete_original_response()
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(embed=discord.Embed(description=f'Deleted Messages!', color=0x50ff50))

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
