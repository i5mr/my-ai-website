import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os

# إعداد البوت
TOKEN = os.getenv('SHOP_TOKEN') # سمِّ المتغير في Koyeb بهذا الاسم
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def generate_user(length):
    chars = string.ascii_lowercase + string.digits + "._"
    return ''.join(random.choice(chars) for _ in range(length))

@bot.command()
async def find(ctx, length: int, amount: int = 5):
    await ctx.send(f"🚀 **رادار المتجر:** جاري فحص {amount} يوزرات بطول {length}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for _ in range(amount):
        user = generate_user(length)
        platforms = {
            "TikTok": f"https://www.tiktok.com/@{user}",
            "Instagram": f"https://www.instagram.com/{user}/"
        }
        
        embed = discord.Embed(title=f"💎 يوزر مقترح: @{user}", color=0x00ff00)
        for name, url in platforms.items():
            try:
                res = requests.get(url, headers=headers, timeout=3)
                status = "✅ متاح" if res.status_code == 404 else "❌ مأخوذ"
                embed.add_field(name=name, value=status, inline=True)
            except:
                embed.add_field(name=name, value="⚠️ خطأ", inline=True)
        
        await ctx.send(embed=embed)
        await asyncio.sleep(2)

bot.run(TOKEN)
