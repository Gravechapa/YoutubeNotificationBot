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

import sys
from logging import INFO, basicConfig, getLogger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from googleapiclient.discovery import build
from telethon import TelegramClient

from .config import Config, Subscriptions

sch = AsyncIOScheduler()
CONFIG = Config()
SUBS = Subscriptions()

basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO)
LOGS = getLogger(__name__)

try:
    YT = build("youtube", "v3", developerKey=CONFIG.yt_api_key())
    LOGS.info("Successfully connected to YouTube")
except BaseException:
    LOGS.info(str(er))
    sys.exit()

try:
    bot = TelegramClient(None, CONFIG.api_id(), CONFIG.api_hash())
    LOGS.info("Successfully connected to Telegram")
except Exception as e:
    LOGS.info(str(e))
    sys.exit()
