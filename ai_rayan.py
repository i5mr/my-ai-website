import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os

# سحب التوكن من Koyeb
TOKEN = os.getenv('SHOP_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@bot.event
async def on_ready():
    print(f'✅ البوت شغال الآن باسم: {bot.user.name}')

# أمر !shop - يعرض قائمة المتجر
@bot.command()
async def shop(ctx):
    embed = discord.Embed(title="🏪 متجر ريان لليوزرات", description="أهلاً بك في أفضل متجر لفحص اليوزرات!", color=0x2f3136)
    embed.add_field(name="🚀 رادار تيك توك", value="للبدء اكتب: `!find [الطول] [العدد]`\nمثال: `!find 4 5` لفحص 5 يوزرات رباعية.", inline=False)
    embed.set_footer(text="Rayan Tool - Your assistant")
    await ctx.send(embed=embed)

# أمر !find - فحص يوزرات تيك توك
@bot.command()
async def find(ctx, length: int, amount: int = 5):
    if length < 3:
        return await ctx.send("⚠️ يوزرات تيك توك لازم تكون 3 أحرف أو أكثر!")
    
    await ctx.send(f"🔍 جاري فحص {amount} يوزرات... انتظر ثواني.")
    
    for _ in range(amount):
        user = generate_user(length)
        url = f"https://www.tiktok.com/@{user}"
        try:
            # استخدام headers لتجنب الحظر
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            status = "✅ متاح" if res.status_code == 404 else "❌ مأخوذ"
            await ctx.send(f"💎 `@{user}` -> **{status}**")
        except:
            pass
        await asyncio.sleep(2) # تأخير بسيط لتجنب حظر الـ IP
    
    await ctx.send("✅ انتهت عملية الفحص.")

bot.run(TOKEN)
