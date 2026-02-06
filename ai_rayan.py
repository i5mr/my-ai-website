import discord
from discord.ext import commands
import os

TOKEN = os.getenv('SHOP_TOKEN') # اسم المتغير الخاص ببوت المتجر

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'🛒 بوت المتجر شغال باسم: {bot.user.name}')

bot.run(TOKEN)
