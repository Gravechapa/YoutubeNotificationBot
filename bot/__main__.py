#    This file is part of the Youtube Notification distribution.
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
# https://github.com/kaif-00z/YoutubeNotificationBot/blob/main/License>.

import os
import asyncio
import pickle
import datetime
import feedparser
from telethon import Button, events, functions, types
from telethon.tl.types import User, Chat, Channel
from .helper import channel_by_name, channel_info, proper_info_msg
from . import LOGS, CONFIG, SUBS, bot, sch

MEMORY_DB = "yn.db"
if os.path.exists(MEMORY_DB):
    with open(MEMORY_DB, "rb") as db_file:
        MEMORY = pickle.load(db_file)
else:
    MEMORY = []
MEMORY_LIMIT = 10000

LOGS.info("Starting the bot")

try:
    bot.start(bot_token=CONFIG.bot_token())
except Exception as exc:
    LOGS.info(str(exc))

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    async with SUBS.lock:
        SUBS.add_chat(event.chat_id)
    await event.reply(
        f"Hi, `{event.sender.username}`.\n" +
        "This is a YouTube notification bot.\n" +
        "You'll be notified when the YouTube channel, " +
        "you subscribed to, publishes a video or starts a live stream.",
        buttons=[
            [
                Button.url("Source code",
                           url="https://github.com/Gravechapa/YoutubeNotificationBot"),
                Button.url("Origin source code",
                           url="https://github.com/kaif-00z/YoutubeNotificationBot"),
            ],
        ],
    )

@bot.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    async with SUBS.lock:
        SUBS.remove_chat(event.chat_id)
    await event.reply("You unsubscribed from mailing list.")



@bot.on(events.NewMessage(pattern="/add_yt_sub"))
async def add_sub(event):
    if str(event.sender_id) not in CONFIG.owner():
        await event.reply("You don't have permission.")
        return
    split_cmd = event.message.message.split(" ", 1)
    if len(split_cmd) < 2:
        await event.reply("Please specify the channel.")
        return
    yt_channel = split_cmd[1]
    if not len(yt_channel.split(" ")) == 1:
        await event.reply("Bad channel identifier.")
        return
    if yt_channel[0] == '@':
        yt_channel = await channel_by_name(yt_channel[1::])
    async with SUBS.lock:
        SUBS.add_channel(yt_channel)
    await event.reply("YouTube channel added.")

@bot.on(events.NewMessage(pattern="/rm_yt_sub"))
async def rm_sub(event):
    if str(event.sender_id) not in CONFIG.owner():
        await event.reply("You don't have permission.")
        return
    split_cmd = event.message.message.split(" ", 1)
    if len(split_cmd) < 2:
        await event.reply("Please specify the channel.")
        return
    yt_channel = split_cmd[1]
    if not len(yt_channel.split(" ")) == 1:
        await event.reply("Bad channel identifier.")
        return
    async with SUBS.lock:
        SUBS.remove_channel(yt_channel)
    await event.reply("YouTube channel removed.")


@bot.on(events.NewMessage(incoming=True, pattern="/subs_info"))
async def sub_info(event):
    text = "**List of subscriptions**\n\n"
    async with SUBS.lock:
        for channel_id in SUBS.channels():
            info = await channel_info(channel_id)
            text += f"`{channel_id}` • `{info['items'][0]['snippet']['title']}`\n"
    await event.reply(text)
    
@bot.on(events.NewMessage(incoming=True, pattern="/mailing_list"))
async def mailing_list(event):
    if str(event.sender_id) not in CONFIG.owner():
        await event.reply("You don't have permission.")
        return
    text = "**Mailing list**\n\n"
    async with SUBS.lock:
        for chat_id in SUBS.chats():
            entity = await bot.get_entity(chat_id)
            text += f"`{chat_id}` • "
            if isinstance(entity, User):
                text += f"`{entity.first_name} {entity.last_name}` `{entity.username}`"
            if isinstance(entity, Chat):
                text += f"`{entity.title}`"
            if isinstance(entity, Channel):
                text += f"`{entity.title}` `{entity.username}`"
            text += '\n'
    await event.reply(text)

async def prepare():
    await bot(functions.bots.SetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code='en',
            commands=[types.BotCommand(
                        command='start',
                        description='Subscribe'),
                    types.BotCommand(
                        command='stop',
                        description='Unsubscribe'),
                    types.BotCommand(
                        command='subs_info',
                        description='List of YouTube subscriptions'),
                    types.BotCommand(
                        command='mailing_list',
                        description='List subscribers. Admin only'),
                    types.BotCommand(
                        command='add_yt_sub',
                        description='Add YouTube subscription. Admin only.'),
                    types.BotCommand(
                        command='rm_yt_sub',
                        description='Remove YouTube subscription. Admin only.')]))

async def forever_check():
    global MEMORY
    async with SUBS.lock:
        local_channels = SUBS.channels().copy()
    for channel_id in local_channels:
        feed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
        for entry in feed.entries:
            yt_link = entry.yt_videoid
            found = False
            for link in reversed(MEMORY):
                if link[0] == yt_link:
                    found = True
                    break
            if found:
                break
            MEMORY.append([yt_link, False])

    async with SUBS.lock:
        local_chats = SUBS.chats().copy()
    for link in MEMORY:
        if not link[1]:
            for chat in local_chats:
                await proper_info_msg(bot, chat, link[0])
                await asyncio.sleep(3)
            link[1] = True

    if len(MEMORY) > MEMORY_LIMIT:
        MEMORY = MEMORY[len(MEMORY) - MEMORY_LIMIT::]

    with open(MEMORY_DB, "wb") as db_file:
        pickle.dump(MEMORY,db_file)

sch.add_job(forever_check,
            "interval",
            minutes=5,
            start_date=datetime.datetime.now() - datetime.timedelta(seconds = 298))

bot.loop.run_until_complete(prepare())
LOGS.info("The bot has started")
sch.start()
bot.loop.run_forever()
