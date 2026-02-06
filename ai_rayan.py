import discord
from discord.ext import commands
import requests
import random
import string
import asyncio
import os

# سحب التوكن من Koyeb
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
            discord.SelectOption(label="تيك توك - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="تيك توك - خماسي", value="tiktok_5", emoji="📱"),
            discord.SelectOption(label="انستقرام - خماسي", value="insta_5", emoji="📸"),
            discord.SelectOption(label="ديسكورد - رباعي", value="discord_4", emoji="💬"),
            discord.SelectOption(label="ديسكورد - خماسي", value="discord_5", emoji="💬"),
        ]
        super().__init__(placeholder="اختر المنصة وطول اليوزر للبدء...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        if scanning:
            return await interaction.response.send_message("⚠️ الرادار شغال فعلاً! اكتب `!stop` أولاً.", ephemeral=True)
            
        selection = self.values[0].split('_')
        platform = selection[0]
        length = int(selection[1])
        
        await interaction.response.send_message(f"🚀 تم تشغيل الرادار الشامل:\n🌍 المنصة: **{platform.upper()}**\n📏 الطول: **{length}**\n🛡️ نظام الحماية: **نشط**", ephemeral=True)
        
        scanning = True
        attempts = 0
        
        while scanning:
            user = generate_user(length)
            is_available = False
            attempts += 1
            
            try:
                if platform == "tiktok":
                    res = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                
                elif platform == "insta":
                    res = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    is_available = (res.status_code == 404)
                
                elif platform == "discord":
                    # فحص ديسكورد عبر API عام (بدون توكن يوزر لتجنب الباند)
                    res = requests.get(f"https://discord.com/api/v9/users/{user}", timeout=5)
                    is_available = (res.status_code == 404)

                # إشعار كل 20 محاولة للتأكد أن البوت لم يتوقف
                if attempts % 20 == 0:
                    await interaction.channel.send(f"🔄 جاري الفحص... (محاولات {platform}: {attempts})", delete_after=2)

                if is_available:
                    embed = discord.Embed(title="🎯 صيدة جديدة!", color=0x00ff00)
                    embed.add_field(name="المنصة", value=platform.capitalize(), inline=True)
                    embed.add_field(name="اليوزر", value=f"`@{user}`", inline=True)
                    embed.set_footer(text="بواسطة ريان تـول")
                    await interaction.channel.send(content="@everyone", embed=embed)
            except:
                pass
            
            # وقت انتظار آمن (3 ثواني) لتجنب الحظر 429
            await asyncio.sleep(3)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MultiPlatformSelect())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} متصل وجاهز للصيد!')

@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="🛠️ لوحة التحكم - ريان تـول",
        description="اختر المنصة ونوع اليوزر من القائمة المنسدلة لبدء الفحص التلقائي.",
        color=0x2f3136
    )
    await ctx.send(embed=embed, view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 تم إيقاف الرادار بنجاح.")

bot.run(TOKEN)
