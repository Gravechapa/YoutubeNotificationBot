# YouTube Notification Bot
**A Telegram bot that will notify you about new videos on selected channels**

## Features
- Can monitor multiple YouTube channels.
- Filter content by regex.
- Can mail to multiple chats.

## Usage
- `/start` - Subscribe to mailing.
- `/stop` - Unsubscribe.
- `/subs_info` - List of YouTube subscriptions.
#### Only for owner
- `/mailing_list` - List of subscribers.
- `/add_yt_sub` - Add YouTube subscription. <br />Channel id or handle(poor precision)(`/add_yt_sub UCWOA1ZGywLbqmigxE4Qlvuw` or `/add_yt_sub @Netflix`).
- `/rm_yt_sub` - Remove YouTube subscription. Channel id or handle.

You need to configure the bot by `config.json` and `subscriptions.json` in order to use it.

**Based on https://github.com/kaif-00z/YoutubeNotificationBot**
