import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os

# التوكن من إعدادات Koyeb
TOKEN = os.getenv('SHOP_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} جاهز لاستلام الأوامر!')

# أمر المتجر
@bot.command()
async def shop(ctx):
    embed = discord.Embed(title="🛒 متجر ريان لليوزرات", description="اطلب يوزرك المفضل الآن!", color=0x00ff00)
    embed.add_field(name="الأوامر المتاحة:", value="`!find [الطول] [العدد]`\nمثال: `!find 4 5` لفحص 5 يوزرات رباعية", inline=False)
    await ctx.send(embed=embed)

# أمر فحص اليوزرات (الرادار)
@bot.command()
async def find(ctx, length: int, amount: int = 5):
    if length < 3:
        return await ctx.send("⚠️ أقل طول ليوزر تيك توك هو 3!")
    
    msg = await ctx.send(f"🚀 جاري فحص {amount} يوزرات... انتظر قليلاً")
    
    for _ in range(amount):
        user = generate_user(length)
        url = f"https://www.tiktok.com/@{user}"
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            status = "✅ متاح" if res.status_code == 404 else "❌ مأخوذ"
            await ctx.send(f"💎 `@{user}` -> **{status}**")
        except:
            pass
        await asyncio.sleep(1.5)
    await ctx.send("✨ تم الانتهاء من الفحص!")

bot.run(TOKEN)
