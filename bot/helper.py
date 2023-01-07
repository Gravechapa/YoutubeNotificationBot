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

import re
from telethon import Button
from . import CONFIG, YT

if CONFIG.name_filter()["case_sensetive"]:
    NAME_FILTER = re.compile(CONFIG.name_filter()["regex"])
else:
    NAME_FILTER = re.compile(CONFIG.name_filter()["regex"], re.IGNORECASE)

def dur_parser(_time):
    if not _time:
        return "Not found!"
    xx = _time.replace("PT", "")
    return xx.lower()

async def channel_by_handle(handle):
    result = YT.search().list(part="id", maxResults=1, q=handle, type="channel").execute()['items']
    if len(result):
        return result[0]['id']['channelId']

async def channel_info(ch_id):
    return (
        YT.channels().list(part="statistics,snippet,contentDetails", id=ch_id).execute()
    )


def video_info(_id):
    return YT.videos().list(part="snippet,contentDetails,statistics", id=_id).execute()

async def proper_info_msg(client, to_id, yt_id):
    info = video_info(yt_id)["items"][0]
    channel_name = info["snippet"]["channelTitle"]
    video_title = info["snippet"]["title"]
    if not NAME_FILTER.match(video_title):
        return
    try:
        desc = info["snippet"]["description"]
        if len(desc) > 500:
            desc = desc[:300] + "..."
    except BaseException:
        desc = "Not found!"
    pub_time = info["snippet"]["publishedAt"].replace("T", " ").replace("Z", " ")
    try:
        thumb = info["snippet"]["thumbnails"]["maxres"]["url"]
    except BaseException:
        thumb = info["snippet"]["thumbnails"]["high"]["url"]
    try:
        dur = dur_parser(info["contentDetails"]["duration"])
    except BaseException:
        dur = "Not found!"
    text = ""
    if info["snippet"]["liveBroadcastContent"] == "live":
        text += f"**{channel_name} is live 🔴**\n\n"
        dur = "♾"
    else:
        text += f"**{channel_name} just uploaded a video**\n\n"
    text += f"```Title - {video_title}\n"
    text += f"Description - {desc}\n"
    text += f"Duration - {dur}\n"
    text += f"Published at - {pub_time}```\n"
    await client.send_file(
        to_id,
        file=f"{thumb}",
        caption=text,
        buttons=[[Button.url("Watch", url=f"https://www.youtube.com/watch?v={yt_id}")]],
    )
