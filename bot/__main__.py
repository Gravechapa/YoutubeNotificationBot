#    This file is part of the Youtube Notification  distribution.
#    Copyright (c) 2022 kaif_00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/kaif-00z/YoutubeNotificationBot/blob/main/License> .


from . import *
from .helper import *

LOGS.info("Starting the bot")

try:
    bot.start(bot_token=CONFIG.bot_token())
except Exception as exc:
    LOGS.info(str(exc))


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"Hi, `{event.sender.first_name}`.\nThis is a YouTube notification bot.\nYou'll be notified when the YouTube channel, you subscribed to, publishes a video or starts a live stream.",
        buttons=[
            [
                Button.url("SOURCE CODE", url="github.com/Kaif-00z/"),
                Button.url("DEVELOPER", url="t.me/kaif_00z"),
            ],
        ],
    )


@bot.on(events.NewMessage(incoming=True, pattern="/subs_info"))
async def sub_info(event):
    if str(event.sender_id) not in CONFIG.owner():
        return
    text = "**List of subscriptions**\n\n"
    for id in SUBS.channels():
        info = await channel_info(id)
        text += f"`• {info['items'][0]['snippet']['title']}`\n"
    await event.reply(text)

FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id="
async def save_it():
    for id in SUBS.channels():
        feed = feedparser.parse(FEED_URL + id)
        yt_link = feed.entries[0].yt_videoid
        if yt_link not in MEMORY:
            MEMORY.append(yt_link)


async def forever_check():
    global MEMORY
    for id in SUBS.channels():
        feed = feedparser.parse(FEED_URL + id)
        yt_link = feed.entries[0].yt_videoid
        if yt_link not in MEMORY:
            await proper_info_msg(bot, SUBS.chats()[0], yt_link)
            MEMORY.append(yt_link)
        if len(MEMORY) > MEMORY_LIMIT:
            MEMORY = MEMORY[len(MEMORY) - MEMORY_LIMIT::]
        await asyncio.sleep(0.5)


sch.add_job(forever_check, "interval", seconds=30)

LOGS.info("The bot has started")
bot.loop.run_until_complete(save_it())
sch.start()
bot.loop.run_forever()
