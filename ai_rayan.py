import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio
from flask import Flask
from threading import Thread

# --- إعداد Flask لضمان استمرار عمل البوت على Koyeb ---
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run():
    # المنفذ 8080 هو الافتراضي لـ Koyeb
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات بوت الديسكورد ---
intents = discord.Intents.default()
intents.message_content = True  # ضروري جداً عشان أمر "ش"

bot = commands.Bot(command_prefix="", intents=intents)

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'✅ سجلنا دخول باسم: {bot.user.name}')

@bot.command(name="ش")
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("⚠️ يا غالي ادخل روم صوتي أول!")

    channel = ctx.author.voice.channel
    
    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
                url = info['url']
                title = info['title']
            except Exception as e:
                return await ctx.send(f"❌ ما قدرت ألقى الأغنية: {e}")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

    await ctx.send(f"🎶 جاري تشغيل: **{title}**")

@bot.command(name="طلع")
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 نراكم على خير!")
    else:
        await ctx.send("أنا مو متصل بأي روم!")

# --- تشغيل النظام المزدوج ---
if __name__ == "__main__":
    keep_alive()  # تشغيل سيرفر الويب في الخلفية
    token = os.getenv('token')  # تأكد أن الاسم في Koyeb هو token
    if token:
        bot.run(token)
    else:
        print("❌ خطأ: لم يتم العثور على التوكن في Environment Variables")
