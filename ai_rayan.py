import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- كود منع الإغلاق التلقائي (Keep Alive) ---
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()
# -------------------------------------------

TOKEN = os.getenv('SHOP_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

scanning = False

def generate_user(length):
    char_set = string.ascii_lowercase + string.digits
    return ''.join(random.choice(char_set) for _ in range(length))

class MultiPlatformSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="TikTok - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="Instagram - خماسي", value="insta_5", emoji="📸"),
            discord.SelectOption(label="Discord - رباعي", value="discord_4", emoji="💬"),
        ]
        super().__init__(placeholder="اختر المنصة وابدأ الصيد...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        if scanning:
            return await interaction.response.send_message("⚠️ الرادار شغال حالياً! أوقفه أولاً بـ !stop", ephemeral=True)
            
        selection = self.values[0].split('_')
        platform, length = selection[0], int(selection[1])
        await interaction.response.send_message(f"🚀 تم بدء رادار **{platform.upper()}** بنجاح!", ephemeral=True)
        
        scanning = True
        while scanning:
            user = generate_user(length)
            is_available = False
            try:
                if platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                elif platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                elif platform == "discord":
                    res = requests.get(f"https://discord.com/api/v9/users/{user}", timeout=5)
                    is_available = (res.status_code == 404)

                if is_available:
                    await interaction.channel.send(f"@everyone 🎯 **صيد جديد!** المنصة: {platform} | اليوزر: `@{user}`")
            except: pass
            await asyncio.sleep(4) # وقت أمان لتجنب الباند 429

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MultiPlatformSelect())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} متصل الآن 24/7!')

@bot.command()
async def setup(ctx):
    embed = discord.Embed(title="🛠️ لوحة تحكم ريان", description="اختر المنصة لبدء الصيد اللانهائي", color=0x2f3136)
    await ctx.send(embed=embed, view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 تم إيقاف الرادار.")

# تشغيل الويب سيرفر قبل البوت
keep_alive()
bot.run(TOKEN)
