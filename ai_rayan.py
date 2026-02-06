import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- نظام Keep Alive لمنع Koyeb من إطفاء البوت ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

def run_web():
    app.run(host='0.0.0.0', port=8000) # لاحظ غيرنا البورت لـ 8000 ليطابق الصورة

def keep_alive():
    t = Thread(target=run_web)
    t.start()
# ---------------------------------------------

TOKEN = os.getenv('SHOP_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

scanning = False

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

class MultiPlatformSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="تيك توك - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="انستقرام - خماسي", value="insta_5", emoji="📸"),
            discord.SelectOption(label="ديسكورد - رباعي", value="discord_4", emoji="💬"),
        ]
        super().__init__(placeholder="اختر المنصة وابدأ الصيد...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        if scanning:
            return await interaction.response.send_message("⚠️ الرادار يعمل بالفعل! أوقفه بـ !stop", ephemeral=True)
            
        selection = self.values[0].split('_')
        platform, length = selection[0], int(selection[1])
        await interaction.response.send_message(f"🚀 بدأ الرادار الآمن لـ **{platform.upper()}**", ephemeral=True)
        
        scanning = True
        while scanning:
            user = generate_user(length)
            is_available = False
            try:
                # نظام فحص ذكي مع تأخير أكبر لتجنب الخطأ 429
                if platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                elif platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                elif platform == "discord":
                    # فحص ديسكورد يحتاج هدوء تام
                    res = requests.get(f"https://discord.com/api/v9/users/{user}", timeout=5)
                    is_available = (res.status_code == 404)

                if is_available:
                    await interaction.channel.send(f"@everyone 🎯 **صيد جديد!** المنصة: {platform} | اليوزر: `@{user}`")
            except: pass
            
            # رفعنا وقت الانتظار لـ 6 ثواني لضمان عدم تكرار الحظر
            await asyncio.sleep(6)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MultiPlatformSelect())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} متصل ومحمي من الإغلاق!')

@bot.command()
async def setup(ctx):
    await ctx.send(embed=discord.Embed(title="🛠️ رادار ريان", description="اختر المنصة للبدء"), view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الصيد.")

# تشغيل السيرفر ثم البوت
keep_alive()
bot.run(TOKEN)
