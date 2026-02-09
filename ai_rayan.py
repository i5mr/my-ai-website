import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os
from flask import Flask
from threading import Thread

# --- نظام الحماية من النوم (Keep Alive) بورت 8000 ---
app = Flask('')
@app.route('/')
def home(): return "Pro Hunter is Active! 🎯"
def run_web(): app.run(host='0.0.0.0', port=8000)
def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

TOKEN = os.getenv('SHOP_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
scanning = False
selected_platform = None

# توليد يوزرات "فخمة" فقط (i5mr, jmay, r_x7)
def generate_pro_user():
    patterns = [
        lambda: random.choice(string.ascii_lowercase) + str(random.randint(0,9)) + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase),
        lambda: random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase),
    ]
    return random.choice(patterns)()

class ProHunter(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="1️⃣ حدد المنصة (انستا / تيك توك / سناب)",
        options=[
            discord.SelectOption(label="Instagram", value="insta", emoji="📸"),
            discord.SelectOption(label="TikTok", value="tiktok", emoji="📱"),
            discord.SelectOption(label="Snapchat", value="snap", emoji="👻")
        ]
    )
    async def platform_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        global selected_platform
        selected_platform = select.values[0]
        await interaction.response.send_message(f"✅ تم اختيار **{selected_platform.upper()}**. اضغط الزر لبدء الصيد الحقيقي!", ephemeral=True)

    @discord.ui.button(label="🎯 بدء الصيد الفعلي", style=discord.ButtonStyle.danger)
    async def start_hunt(self, interaction: discord.Interaction, button: discord.ui.Button):
        global scanning, selected_platform
        if not selected_platform: return await interaction.response.send_message("⚠️ حدد المنصة أولاً!", ephemeral=True)
        
        scanning = True
        await interaction.response.send_message(f"🚀 الرادار يعمل الآن 24/7 على {selected_platform}. سيتم إرسال الصيدات الحقيقية فقط!", ephemeral=True)
        
        while scanning:
            user = generate_pro_user()
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                
                # فحص انستقرام
                if selected_platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers=headers, timeout=5)
                    # إذا 404 يعني اليوزر متاح "صدق"
                    if res.status_code == 404:
                        await interaction.channel.send(f"🔥 @everyone **صيدة انستا حقيقية!**\nالـيـوزر: `@{user}`")
                
                # فحص تيك توك
                elif selected_platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers=headers, timeout=5)
                    if res.status_code == 404:
                        await interaction.channel.send(f"📱 @everyone **صيدة تيك توك حقيقية!**\nالـيـوزر: `@{user}`")

            except Exception as e:
                print(f"Error: {e}")
            
            # أهم نقطة: وقت انتظار 12 ثانية عشان ما تنحظر وتضيع عليك الصيدة
            await asyncio.sleep(12)

@bot.command()
async def setup(ctx):
    await ctx.send(embed=discord.Embed(title="🛡️ رادار ريان - نسخة الصيد الحقيقي", description="هذه النسخة مبرمجة لتجنب الحظر والصيد بدقة عالية.", color=0xFF0000), view=ProHunter())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الصيد.")

if __name__ == "__main__":
    keep_alive() # يمنع حالة الـ Sleeping
    bot.run(TOKEN)
