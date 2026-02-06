import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- 1. نظام الحماية من الإغلاق (24 ساعة) ---
app = Flask('')
@app.route('/')
def home():
    return "The Guard is Online 24/7!"

def run_web():
    # البورت 8000 ليتوافق مع إعدادات Koyeb الافتراضية
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- 2. إعدادات البوت ---
TOKEN = os.getenv('SHOP_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

scanning = False

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

class MultiPlatformSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="TikTok - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="Instagram - خماسي", value="insta_5", emoji="📸"),
            discord.SelectOption(label="Discord - رباعي", value="discord_4", emoji="💬"),
        ]
        super().__init__(placeholder="اختر الهدف لبدء الصيد...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        if scanning:
            return await interaction.response.send_message("⚠️ الرادار يعمل بالفعل! أوقفه بـ !stop", ephemeral=True)
            
        selection = self.values[0].split('_')
        platform, length = selection[0], int(selection[1])
        await interaction.response.send_message(f"🛡️ بدأ الرادار المحمي لـ **{platform.upper()}**\nسيعمل البوت 24 ساعة حتى لو أغلقت المتصفح.", ephemeral=True)
        
        scanning = True
        while scanning:
            user = generate_user(length)
            is_available = False
            try:
                # فحص تيك توك
                if platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                
                # فحص انستقرام
                elif platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                
                # فحص ديسكورد (نظام آمن)
                elif platform == "discord":
                    res = requests.get(f"https://discord.com/api/v9/users/{user}", timeout=5)
                    is_available = (res.status_code == 404)

                if is_available:
                    await interaction.channel.send(f"@everyone 🎯 **صيد جديد ومحمي!**\nالمنصة: **{platform.capitalize()}**\nاليوزر: `@{user}`")
            except: 
                pass # في حال حدوث أي خطأ، الكود سيستمر ولن يتوقف
            
            # وقت انتظار آمن جداً (5 ثواني) لضمان عدم الحظر نهائياً
            await asyncio.sleep(5)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MultiPlatformSelect())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} تحت الحماية القصوى ويعمل الآن!')

@bot.command()
async def setup(ctx):
    embed = discord.Embed(title="🛡️ لوحة تحكم ريان (النسخة المحمية)", description="اختر المنصة لبدء الصيد التلقائي 24/7", color=0x2b2d31)
    await ctx.send(embed=embed, view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الرادار.")

# تشغيل نظام منع الإغلاق ثم تشغيل البوت
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
