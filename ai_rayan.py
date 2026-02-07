import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- نظام منع النوم (Keep Alive) لضمان العمل 24 ساعة ---
app = Flask('')
@app.route('/')
def home(): return "Multi-Menu Radar is Live! 🎯"
def run_web(): app.run(host='0.0.0.0', port=8000)
def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- إعدادات البوت ---
TOKEN = os.getenv('SHOP_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

scanning = False
selected_platform = None

class HuntView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # القائمة الأولى: المنصات
    @discord.ui.select(
        placeholder="1️⃣ اختر المنصة المراد صيدها...",
        options=[
            discord.SelectOption(label="TikTok", value="tiktok", emoji="📱"),
            discord.SelectOption(label="Instagram", value="insta", emoji="📸"),
            discord.SelectOption(label="Snapchat", value="snap", emoji="👻"),
            discord.SelectOption(label="Discord", value="discord", emoji="💬")
        ]
    )
    async def platform_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        global selected_platform
        selected_platform = select.values[0]
        await interaction.response.send_message(f"✅ اخترت **{selected_platform.upper()}**. الحين حدد طول اليوزر من القائمة اللي تحت 👇", ephemeral=True)

    # القائمة الثانية: الطول
    @discord.ui.select(
        placeholder="2️⃣ اختر طول اليوزر (ثلاثي، رباعي، خماسي)...",
        options=[
            discord.SelectOption(label="يوزر ثلاثي (نادر)", value="3"),
            discord.SelectOption(label="يوزر رباعي", value="4"),
            discord.SelectOption(label="يوزر خماسي", value="5")
        ]
    )
    async def length_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        global scanning, selected_platform
        if not selected_platform:
            return await interaction.response.send_message("⚠️ يا ريان، لازم تختار المنصة أولاً من القائمة فوق!", ephemeral=True)
        
        length = int(select.values[0])
        await interaction.response.send_message(f"🚀 بدأ الرادار: **{selected_platform.upper()}** | الطول: **{length}**\nسيتم إرسال الفحص ومنشن عند الصيد!", ephemeral=True)
        
        scanning = True
        while scanning:
            user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
            try:
                # إرسال اليوزر الحالي للتأكد أن البوت ليس في حالة Sleeping
                check_msg = await interaction.channel.send(f"🔍 فحص {selected_platform}: `@{user}`")
                
                # فحص المنصات
                if selected_platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                elif selected_platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                elif selected_platform == "snap":
                    res = requests.get(f"https://www.snapchat.com/add/{user}", timeout=5)
                elif selected_platform == "discord":
                    res = requests.get(f"https://discord.com/api/v9/users/{user}", timeout=5)

                if res.status_code == 404:
                    await interaction.channel.send(f"@everyone 🎯 **صيدة جديدة!**\nالمنصة: {selected_platform}\nاليوزر: `@{user}`")
                
                await asyncio.sleep(1) # تأخير بسيط قبل حذف رسالة الفحص
                await check_msg.delete()
                
            except: pass
            
            # وقت انتظار 10 ثوانٍ لضمان عدم تكرار حظر 429
            await asyncio.sleep(10)

@bot.command()
async def setup(ctx):
    embed = discord.Embed(title="🛡️ رادار ريان الاحترافي", description="حدد خياراتك لبدء الصيد التلقائي 24/7", color=0x2b2d31)
    await ctx.send(embed=embed, view=HuntView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الرادار.")

if __name__ == "__main__":
    keep_alive() # تشغيل نظام الحماية من النوم
    bot.run(TOKEN)
