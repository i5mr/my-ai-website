import discord
from discord.ext import commands
import os

# سحب التوكن من إعدادات السيرفر (Koyeb)
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ تم تشغيل البوت المدمج باسم: {bot.user.name}')
    print('🛒 نظام المتجر: فعال')
    print('💻 نظام الهكر: فعال')

# --- [ قسم أوامر المتجر ] ---
@bot.command()
async def shop(ctx):
    await ctx.send("🏪 قائمة المتجر قيد التجهيز... اطلب ما تريد!")

# --- [ قسم أوامر الهكر ] ---
@bot.command()
async def hack(ctx, member: discord.Member):
    await ctx.send(f"⚠️ جاري محاكاة اختراق {member.name}... [██████████] 100%")
    await ctx.send("✅ تمت العملية بنجاح (مجرد مزحة!)")

# --- [ أوامر عامة ] ---
@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 شغال تمام! الاستجابة: {round(bot.latency * 1000)}ms')

# تشغيل البوت باستخدام التوكن السري
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ خطأ: التوكن غير موجود في إعدادات Koyeb!")
