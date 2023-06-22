# MyPersBot

Python-based Telegram Bot which uses native Telegram API

## Preparetions

You have to create a config file **bot_conf.py** in the same directory where will be located script:
```
#TG token - DO NOT share this info:
token = '<token without 'bot'>';

#Log function settings:
log_file = '/var/log/bot.log';

#HTTP settings:
http_timeout = 5;
http_timeout_read = 10;
```

You can create linux service from this script **bot_start.py** and run it in a background.

Enjoy!
