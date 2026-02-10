import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

# إعدادات الصلاحيات (Intents)
intents = discord.Intents.default()
intents.message_content = True

# جعل البريفكس فارغ ليعمل مع حرف "ش" مباشرة
bot = commands.Bot(command_prefix="", intents=intents)

# إعدادات مستخرج الفيديو (yt-dlp)
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'✅ تم تشغيل البوت بنجاح: {bot.user.name}')

@bot.command(name="ش")
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("⚠️ لازم تدخل روم صوتي أولاً!")

    channel = ctx.author.voice.channel
    
    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                # يدعم البحث بالاسم أو الرابط
                info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
                url = info['url']
                title = info['title']
            except Exception as e:
                return await ctx.send(f"❌ حدث خطأ أثناء البحث: {e}")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

    await ctx.send(f"🎶 جاري تشغيل: **{title}**")

@bot.command(name="طلع")
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 تم فصل البوت.")
    else:
        await ctx.send("البوت مو متصل بروم!")

# تأكد أن الكلمة داخل القوسين تطابق الاسم اللي حطيته في Koyeb

token = os.getenv('DISCORD_TOKEN')

bot.run('ضع_التوكن_هنا_بين_العلامات')

