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

import json

class Config:
    def __init__(self):
        try:
            with open("config.json", "r") as config_file:
                self.__data = json.load(config_file)
                config_file.close()
            if not self.__data["api_id"] or not self.__data["api_hash"]:
                self.__data["api_id"] = 6
                self.__data["api_hash"] = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
            if not self.__data["name_filter"]["regex"]:
                self.__data["name_filter"]["regex"] = ".*"
            if not self.__data["bot_token"] or not self.__data["yt_api_key"]:
                raise Exception("bot_token or yt_api_key is not set") 
            
        except Exception as e:
            LOGS.info("Config parsing failed")
            LOGS.info(str(e))
            exit()

    def api_id(self):
        return self.__data["api_id"]
    def api_hash(self):
        return self.__data["api_hash"]
    def bot_token(self):
        return self.__data["bot_token"]
    def owner(self):
        return self.__data["owner"]
    def yt_api_key(self):
        return self.__data["yt_api_key"]
    def name_filter(self):
        return self.__data["name_filter"]

class Subscriptions:
    def __init__(self):
        try:
            with open("subscriptions.json", "r") as subscriptions_file:
                self.__data = json.load(subscriptions_file)
                subscriptions_file.close()
            
        except Exception as e:
            LOGS.info("Subscriptions parsing failed")
            LOGS.info(str(e))
            exit()

    def __updateJson(self):
        try:
            with open("subscriptions.json", "w") as subscriptions_file:
                json.dump(self.__data, subscriptions_file)
                subscriptions_file.close()
            
        except Exception as e:
            LOGS.info("Subscriptions write failed")
            LOGS.info(str(e))
    
    def chats(self):
        return self.__data["chats"]
    def channels(self):
        return self.__data["yt_channel_ids"]

    def add_chat(self, chat_id):
        self.__data["chats"].append(chat_id)
        __updateJson()
    def add_channel(self, channel_id):
        self.__data["yt_channel_ids"].append(channel_id)
        __updateJson()
    def remove_chat(self, chat_id):
        self.__data["chats"].remove(chat_id)
        __updateJson()
    def remove_channel(self, channel_id):
        self.__data["yt_channel_ids"].remove(channel_id)
        __updateJson()
