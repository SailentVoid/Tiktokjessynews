import os
import asyncio
import discord
import feedparser

TOKEN = os.getenv("DISCORD-BOT")  # токен берём из Railway переменной
CHANNEL_ID = 1423046960948052159  # твой ID канала Discord
TIKTOK_RSS = "https://rss.app/feeds/RtLH49NY2PjfcAzR.xml"  # твой RSS фид

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_video = None

async def check_tiktok():
    global last_video
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        feed = feedparser.parse(TIKTOK_RSS)
        if feed.entries:
            latest = feed.entries[0]
            if last_video != latest.link:
                last_video = latest.link
                await channel.send(f"🎥 Новый TikTok: {latest.title}\n{latest.link}")
        await asyncio.sleep(300)  # каждые 5 минут проверка

@client.event
async def on_ready():
    print(f"✅ Бот запущен как {client.user}")

client.loop.create_task(check_tiktok())
client.run(TOKEN)
