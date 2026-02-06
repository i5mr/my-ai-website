import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os

# تأكد أنك سميت المتغير في Koyeb بهذا الاسم: SHOP_TOKEN
TOKEN = os.getenv('SHOP_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@bot.event
async def on_ready():
    print(f'🛒 بوت المتجر (الرادار) شغال باسم: {bot.user.name}')

@bot.command()
async def find(ctx, length: int, amount: int = 5):
    if length < 3:
        return await ctx.send("⚠️ اليوزرات في تيك توك لازم تكون 3 أحرف أو أكثر!")
    
    await ctx.send(f"🚀 **رادار المتجر:** جاري فحص {amount} يوزرات بطول {length}...")
    
    for _ in range(amount):
        user = generate_user(length)
        url = f"https://www.tiktok.com/@{user}"
        try:
            # إضافة headers لمحاكاة متصفح حقيقي وتجنب الحظر
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            status = "✅ متاح أو محذوف" if res.status_code == 404 else "❌ مأخوذ"
            await ctx.send(f"💎 اليوزر: `@{user}` -> **{status}**")
        except:
            await ctx.send(f"⚠️ تعذر فحص اليوزر `@{user}` (مشكلة في الشبكة)")
        
        await asyncio.sleep(2) # تأخير عشان ما يحظرك تيك توك

bot.run(TOKEN)
