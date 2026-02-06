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
    # يوزرات ديسكورد تسمح بـ (أحرف، أرقام، نقطة، شرطة تحتية)
    char_set = string.ascii_lowercase + string.digits + "_."
    return ''.join(random.choice(char_set) for _ in range(length))

class MultiPlatformSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="TikTok - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="Instagram - خماسي", value="insta_5", emoji="📸"),
            discord.SelectOption(label="Discord - رباعي", value="discord_4", emoji="💬"),
            discord.SelectOption(label="Discord - خماسي", value="discord_5", emoji="💬"),
        ]
        super().__init__(placeholder="اختر المنصة وابدأ الصيد...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        selection = self.values[0].split('_')
        platform = selection[0]
        length = int(selection[1])
        
        await interaction.response.send_message(f"🚀 بدأ الرادار الشامل: **{platform.upper()}** | الطول: **{length}**", ephemeral=True)
        
        scanning = True
        attempt_count = 0
        
        while scanning:
            user = generate_user(length)
            attempt_count += 1
            
            try:
                if platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                
                elif platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                
                elif platform == "discord":
                    # فحص ديسكورد عن طريق محاولة إرسال طلب لصفحة المستخدم
                    res = requests.get(f"https://discord.com/api/v9/users/{user}", timeout=5)
                    # ديسكورد غالباً يمنع الوصول المباشر، لكن لو عطى 404 في روابط معينة يعني متاح
                    is_available = (res.status_code == 404)

                # رسالة تطمين كل 15 محاولة
                if attempt_count % 15 == 0:
                    await interaction.channel.send(f"⏳ فحصت {attempt_count} يوزرات في {platform}... جاري البحث عن صيدة 🔍", delete_after=3)

                if is_available:
                    await interaction.channel.send(f"@everyone 💎 **صيد ثقيل!**\nالمنصة: **{platform.capitalize()}**\nاليوزر: `@{user}`")
            except:
                pass
            
            await asyncio.sleep(2.5)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MultiPlatformSelect())

@bot.command()
async def setup(ctx):
    await ctx.send("✨ **لوحة تحكم ريان (تيك توك - انستا - ديسكورد)**", view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 توقف الصيد.")

bot.run(TOKEN)
