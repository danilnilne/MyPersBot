import time
import requests;
import bot_conf;
import dolog;
import json

token = bot_conf.token;
http_timeout = bot_conf.http_timeout;
http_timeout_read = bot_conf.http_timeout_read;

### GetUpdate function. This fucntion request updates from TAPI.
def GetUpdate(token):

    url = 'https://api.telegram.org/bot' + token + '/' + 'getUpdates';

    try:

        response = requests.get(url, timeout=(http_timeout, http_timeout_read));

    except requests.exceptions.RequestException as e:

        dolog.WriteLog(GetUpdate.__name__ + ' - ' + str(e));

    else:

        return response;
# GetUpdate END

### SendMessage function. This fucntion sends data to the chat using TAPI.
def SendMessage(token, update):

    chat_id = str(update['message']['chat']['id']);

    bot_reply = str(update['message']['bot_reply']);

    #https://api.telegram.org/bot[BOT_API_KEY]/sendMessage?chat_id=[MY_CHANNEL_NAME]&text=[MY_MESSAGE_TEXT]
    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&text=' + bot_reply;

    dolog.WriteLog(SendMessage.__name__ + ' - ' + url);

    #Send Message to the chat
    try:

        response = requests.post(url, timeout=(http_timeout, http_timeout_read));

    except requests.exceptions.RequestException as e:

        dolog.WriteLog(SendMessage.__name__ + ' - ' + str(e));

    else:

        #Mark Update as resolved

        offset = str(update['update_id'] + 1);

        url = 'https://api.telegram.org/bot' + token + '/' + 'getUpdates?offset=' + offset;

        try:

            response = requests.post(url, timeout=(http_timeout, http_timeout_read));

        except requests.exceptions.RequestException as e:

            dolog.WriteLog(SendMessage.__name__ + ' - ' + str(e));

        else:

            return 0;

# SendMessage END

### ParseUpdate function. This fucntion unparse values from the GetUpdate response.
def ParseUpdate(response):

    if (response):

        if (response.status_code == 200):

    #        dolog.WriteLog(ParseUpdate.__name__ + ' - ' + 'HTTP Code is 200. Good connection...');

            data = response.json();

            try:

                data['result'];

            except:

                dolog.WriteLog(ParseUpdate.__name__ + ' - ' + 'No updates. Continue GetUpdates');

            else:

#            print(data);           # Debug logging to the console.

                for update in data['result']:

                    ParseCommand(update);

                    dolog.WriteLog(ParseUpdate.__name__ + ' - ' + json.dumps(update, indent=2));

        else:

            dolog.WriteLog(ParseUpdate.__name__ + ' - ' + "HTTP code != 200.");

#            exit(1);

    else:

        dolog.WriteLog(ParseUpdate.__name__ + ' - ' + "HTTP request failed.");

# ParseUpdate END

### ParseCommand function. This fucntion unparse message from the GetUpdate response
### and try to get command.
def ParseCommand(update):

    message_text = str(update['message']['text']);

    if (message_text[:1] == '/'):

        update['message']['bot_reply'] = 'Command: ' + message_text + '-------';

    else:

        update['message']['bot_reply'] = 'Text: ' + message_text + '-------';

    dolog.WriteLog(ParseCommand.__name__ + ' - ' + json.dumps(update, indent=2));

    SendMessage(token, update);
# ParseUpdate END

### Main
while True:

    response = GetUpdate(token);

    ParseUpdate(response);

    time.sleep(3);

# Main END
