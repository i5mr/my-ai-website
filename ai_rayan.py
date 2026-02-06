import discord
from discord.ext import commands
import os
import sys

# محاولة سحب التوكن بأكثر من اسم لضمان العمل
TOKEN = os.getenv('TOKEN') or os.getenv('SHOP_TOKEN') or os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("❌ خطأ: السيرفر لم يجد التوكن في الإعدادات!")
    print("تأكد أنك أضفت متغير في Koyeb باسم TOKEN")
    sys.exit(1) # إيقاف البوت بدلاً من الانهيار

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ تم تسجيل الدخول بنجاح باسم: {bot.user.name}')
    print('🚀 البوت الآن يعمل 24 ساعة على السيرفر')

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 شغال! سرعة الاستجابة: {round(bot.latency * 1000)}ms')

# تشغيل البوت
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"❌ حدث خطأ أثناء الاتصال بديسكورد: {e}")
