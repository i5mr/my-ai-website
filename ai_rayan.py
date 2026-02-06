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
            discord.SelectOption(label="TikTok - ثلاثي", value="tiktok_3", emoji="📱"),
            discord.SelectOption(label="TikTok - رباعي", value="tiktok_4", emoji="📱"),
            discord.SelectOption(label="Instagram - رباعي", value="insta_4", emoji="📸"),
            discord.SelectOption(label="Instagram - خماسي", value="insta_5", emoji="📸"),
        ]
        super().__init__(placeholder="اختر المنصة وطول اليوزر...", options=options)

    async def callback(self, interaction: discord.Interaction):
        global scanning
        selection = self.values[0].split('_')
        platform = selection[0]
        length = int(selection[1])
        
        await interaction.response.send_message(f"🚀 بدأ الرادار: **{platform.upper()}** | الطول: **{length}**\nاكتب `!stop` للإيقاف.", ephemeral=True)
        
        scanning = True
        while scanning:
            user = generate_user(length)
            
            if platform == "tiktok":
                url = f"https://www.tiktok.com/@{user}"
                headers = {'User-Agent': 'Mozilla/5.0'}
            else: # Instagram
                url = f"https://www.instagram.com/{user}/"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

            try:
                res = requests.get(url, headers=headers, timeout=5)
                # في تيك توك وانستا غالباً 404 يعني متاح
                if res.status_code == 404:
                    await interaction.channel.send(f"💎 **متاح في {platform}:** `@{user}`")
            except:
                pass
            
            await asyncio.sleep(2.5) # تأخير للحماية من الباند

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MultiPlatformSelect())

@bot.event
async def on_ready():
    print(f'✅ البوت المطور جاهز باسم: {bot.user.name}')

@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="✨ لوحة تحكم الرادار",
        description="اختر من القائمة أدناه المنصة والطول الذي تريد صيده:",
        color=0xFF00D2
    )
    embed.set_footer(text="صنع بواسطة ريان")
    await ctx.send(embed=embed, view=SetupView())

@bot.command()
async def stop(ctx):
    global scanning
    scanning = False
    await ctx.send("🛑 تم إيقاف جميع عمليات الفحص.")

bot.run(TOKEN)
