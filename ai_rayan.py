import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True  # ضروري لقراءة أمر "ش"

bot = commands.Bot(command_prefix="", intents=intents)

# إعدادات التشغيل المباشر بدون تحميل الملف
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is online!')

@bot.command(name="ش")
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("ادخل روم صوتي أول!")
    
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    
    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            url = info['url']
        
        # إذا كان شغال يوقف ويشغل الجديد
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            
        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
        await ctx.send(f"🎶 تشغيل: **{info['title']}**")

@bot.command(name="طلع")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

# جلب التوكن من Koyeb
bot.run(os.getenv('token'))
