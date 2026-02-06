import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- نظام البقاء حياً لمنع حالة Sleeping ---
app = Flask('')
@app.route('/')
def home(): return "Radar is Monitoring Live! 🎯"
def run(): app.run(host='0.0.0.0', port=8000)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- إعدادات البوت ---
TOKEN = os.getenv('SHOP_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
scanning = False

def generate_insta_4():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(4))

@bot.command()
async def start_live(ctx):
    global scanning
    if scanning: return await ctx.send("🛡️ الرادار شغال بالفعل!")
    
    scanning = True
    # رسالة الحالة التي ستتحدث باستمرار
    status_msg = await ctx.send("🚀 بدأ الفحص الحي ليوزرات انستا الرباعية...")
    
    while scanning:
        user = generate_insta_4()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        try:
            # تحديث الرسالة لتبين اليوزر الحالي الذي يتم فحصه
            await status_msg.edit(content=f"🔍 جاري فحص: `@{user}` ...")
            
            res = requests.get(f"https://www.instagram.com/{user}/", headers=headers, timeout=5)
            
            if res.status_code == 404:
                # إذا وجد يوزر متاح يرسل رسالة جديدة ومنشن
                await ctx.send(f"💎 @everyone **صيدة انستا رباعية متاحة!**\nاليوزر: `@{user}`")
            
        except Exception as e:
            print(f"Error during scan: {e}")
        
        # وقت انتظار 8 ثوانٍ لتجنب حظر 429 الظاهر في صورك السابقة
        await asyncio.sleep(8)

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الرادار الحي.")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
