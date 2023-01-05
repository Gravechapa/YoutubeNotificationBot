# YouTube Notification Bot
**A Telegram bot that will notify you about new videos on selected channels**

# Features
- Can monitor multiple YouTube channels.
- Filter content by regex.
- Can mail to multiple chats.

## Usage
- `/start` - Subscribe to mailing.
- `/stop` - Unsubscribe.
- `/subs_info` - List of YouTube subscriptions.
- `/add_yt_sub` - Add YouTube subscription. 
Channel id or name(/add_yt_sub UCWOA1ZGywLbqmigxE4Qlvuw or /add_yt_sub @Netflix). Only for owner.
- `/rm_yt_sub` - Remove YouTube subscription. Channel id. Only for owner.

You need to configure the bot by `config.json` and `subscriptions.json` in order to use it.
