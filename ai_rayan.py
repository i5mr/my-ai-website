import discord
from discord.ext import commands
import yt_dlp
import os
from flask import Flask
from threading import Thread

# --- تشغيل سيرفر ويب بسيط لمنع Koyeb من إغلاق البوت ---
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True', 'quiet': True}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'✅ تم تسجيل الدخول باسم: {bot.user.name}')

@bot.command(name="ش")
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("⚠️ ادخل روم صوتي أولاً!")

    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
                url = info['url']
                title = info['title']
            except Exception as e:
                return await ctx.send(f"❌ خطأ في البحث: {e}")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
    await ctx.send(f"🎶 جاري تشغيل: **{title}**")

@bot.command(name="طلع")
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

if __name__ == "__main__":
    keep_alive()
    # تأكد أنك سميت المتغير في Koyeb باسم token (حروف صغيرة)
    bot.run(os.getenv('token'))
