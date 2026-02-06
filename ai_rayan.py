import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- نظام البقاء حياً 24 ساعة ---
app = Flask('')
@app.route('/')
def home(): return "Instagram Radar is Active!"
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
    # يوزرات انستا الرباعية غالباً تكون أحرف وأرقام ونقطة
    chars = string.ascii_lowercase + string.digits + "."
    return ''.join(random.choice(chars) for _ in range(4))

@bot.command()
async def hunt_insta(ctx):
    global scanning
    if scanning: return await ctx.send("⚠️ الرادار يعمل بالفعل!")
    
    scanning = True
    await ctx.send("🚀 بدأ رادار انستقرام الرباعي 24/7... سيتم المنشن عند الصيد!")
    
    attempts = 0
    while scanning:
        user = generate_insta_4()
        # هيدرز احترافية لتقليد المتصفح الحقيقي وتجنب الباند
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        try:
            url = f"https://www.instagram.com/{user}/"
            res = requests.get(url, headers=headers, timeout=5)
            attempts += 1
            
            # في انستقرام 404 تعني أن الحساب غير موجود (متاح للصيد)
            if res.status_code == 404:
                await ctx.send(f"@everyone 🔥 **صيد انستا رباعي نادر!**\nاليوزر: `@{user}`\nرابط: {url}")
            
            # رسالة طمأنة كل 50 محاولة
            if attempts % 50 == 0:
                print(f"Checked {attempts} Instagram users...")

        except Exception as e:
            print(f"Error: {e}")
        
        # وقت انتظار آمن (6 ثواني) لضمان عدم حظر IP السيرفر 
        await asyncio.sleep(6)

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الرادار.")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
