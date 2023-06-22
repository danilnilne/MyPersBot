# TG token - DO NOT share this info
token = '5950339134:AAFqutcSzVMCvAM6i8CUWGMvupWQwDvbpzU';

# Log function settings
log_file = '/var/log/bot.log';

# Router auth
router_fqdn = "giga.kds.local"
login = "admin"
passw = "9110102"

# HTTP settings
http_timeout = 5;
http_timeout_read = 10;

# DB connection settings
db_user = "admin";
db_password = "Unix0stream";
db_host = "linux.kds.local";
db_port = 3306;
db_name = "kds.local";

# GitHub
gh_password = "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";
# ----------------------------------------------
# Manual testing with link:
#
# https://api.telegram.org/bot5950339134:AAFqutcSzVMCvAM6i8CUWGMvupWQwDvbpzU/getUpdates
#
# Need to handle correctly when:
# Result contains all present UPDATEs:
#
# for update in data['result']:
# JSON.result.[0] - update1
# JSON.result.[1] - update2
# JSON.result.[2] - update3
#
## TEXT messages
# JSON.result.[0]
# JSON.result[0].message.text
#
## STICKER
# JSON.result.[1]
# JSON.result[1].message.sticker
#
## PHOTO
# JSON.result.[2]
# JSON.result[2].message.photo
# ----------------------------------------------