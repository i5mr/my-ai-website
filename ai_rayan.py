import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os

TOKEN = os.getenv('SHOP_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# متغير للتحكم في حالة الفحص (إيقاف أو تشغيل)
scanning = False

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} جاهز للعمل بنظام الـ Setup!')

@bot.command()
async def setup(ctx):
    global scanning
    if scanning:
        return await ctx.send("⚠️ البوت جالس يفحص حالياً، اكتب `!stop` أولاً.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # السؤال الأول: طول اليوزر
        await ctx.send("🔢 **كم حرف تبي طول اليوزر؟** (مثلاً: 3 أو 4)")
        msg1 = await bot.wait_for('message', check=check, timeout=30.0)
        length = int(msg1.content)

        # السؤال الثاني: العدد
        await ctx.send("🔁 **كم يوزر تبي يفحص؟** (اكتب `0` لفحص لا نهائي)")
        msg2 = await bot.wait_for('message', check=check, timeout=30.0)
        amount = int(msg2.content)

        scanning = True
        await ctx.send(f"🚀 تم بدء الرادار! (الطول: {length} | العدد: {'لا نهائي' if amount == 0 else amount})\nلإيقاف الفحص اكتب `!stop`")

        count = 0
        while scanning:
            if amount != 0 and count >= amount:
                break
            
            user = generate_user(length)
            url = f"https://www.tiktok.com/@{user}"
            try:
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                if res.status_code == 404:
                    await ctx.send(f"✅ متاح: `@{user}`")
                # ملاحظة: شلنا رسالة "مأخوذ" عشان ما يزعجك الشات في الفحص اللانهائي
            except:
                pass
            
            count += 1
            await asyncio.sleep(2) # تأخير لضمان عدم الحظر

        scanning = False
        await ctx.send("🏁 انتهى الفحص.")

    except ValueError:
        await ctx.send("❌ خطأ: لازم تكتب أرقام فقط!")
    except asyncio.TimeoutError:
        await ctx.send("⏰ تأخرت في الرد، تم إلغاء الـ Setup.")

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 تم إيقاف الرادار بنجاح.")

bot.run(TOKEN)
