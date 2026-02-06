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

scanning = False

def generate_user(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

class MultiPlatformSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="TikTok - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="TikTok - خماسي", value="tiktok_5", emoji="📱"),
            discord.SelectOption(label="Instagram - خماسي", value="insta_5", emoji="📸"),
        ]
        super().__init__(placeholder="اختر المنصة وابدأ الصيد...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        selection = self.values[0].split('_')
        platform = selection[0]
        length = int(selection[1])
        
        await interaction.response.send_message(f"🚀 بدأ الرادار: **{platform.upper()}** | الطول: **{length}**", ephemeral=True)
        
        scanning = True
        attempt_count = 0 # عداد المحاولات
        
        while scanning:
            user = generate_user(length)
            url = f"https://www.tiktok.com/@{user}" if platform == "tiktok" else f"https://www.instagram.com/{user}/"
            
            try:
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                attempt_count += 1
                
                # كل 10 محاولات، يرسل رسالة "تطمين" في الشات
                if attempt_count % 10 == 0:
                    await interaction.channel.send(f"⏳ رادار {platform}: فحصت {attempt_count} يوزرات مأخوذة حتى الآن... البحث مستمر 🔍", delete_after=5)

                if res.status_code == 404:
                    await interaction.channel.send(f" @everyone 💎 **صيد جديد!**\nالمنصة: {platform}\nاليوزر: `@{user}`")
            except:
                pass
            
            await asyncio.sleep(2)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MultiPlatformSelect())

@bot.command()
async def setup(ctx):
    await ctx.send("✨ **لوحة تحكم ريان**", view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الصيد.")

bot.run(TOKEN)
