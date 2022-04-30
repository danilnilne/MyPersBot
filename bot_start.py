import time
import requests;
import bot_conf;
import dolog;
import json;
import lib_dk;

token = bot_conf.token;
http_timeout = bot_conf.http_timeout;
http_timeout_read = bot_conf.http_timeout_read;

### GetUpdate function. This fucntion requests updates from tAPI.
def GetUpdate(token):

    url = 'https://api.telegram.org/bot' + token + '/' + 'getUpdates';

    try:

        response = requests.get(url, timeout=(http_timeout, http_timeout_read));

    except requests.exceptions.RequestException as e:

        dolog.WriteLog(GetUpdate.__name__ + ' - ' + str(e));

    else:

        return response;
# GetUpdate END

### SendMessage function. This fucntion sends data to the chat using tAPI.
def SendMessage(update):

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
        SendResolve(update);

# SendMessage END

### ParseUpdate function. This fucntion unparses values from the GetUpdate response.
def ParseUpdate(response):

    if (response):

        if (response.status_code == 200):
            #dolog.WriteLog(ParseUpdate.__name__ + ' - ' + 'HTTP Code is 200. Good connection...');
            data = response.json();

            if (data['ok'] == True):

                try:

                    data['result'];

                except:

                    dolog.WriteLog(ParseUpdate.__name__ + ' - ' + 'Incorrect recieved data');

                else:

    #            print(data);           # Debug logging to the console.

                    for update in data['result']:

                        try:

                            update['message'];

                        except:

                            if (update['edited_message']):

                                dolog.WriteLog(ParseUpdate.__name__ + ' - ' + str(update['edited_message']['chat']['id']) + '<--->' + str(update['edited_message']['text']));

                                #update['message']['chat']['id'] = update['edited_message']['chat']['id'];

                                #update['message']['bot_reply'] = "Edited messages don't support for a while";

                                #SendMessage(update);

                            dolog.WriteLog(ParseUpdate.__name__ + ' - ' + "Message " + str(update['edited_message']['chat']['id']) + " block is absent. Looks like it's " + str(update['edited_message']['text']) + " reply. Update will be marked as resolved");

                            SendResolve(update);

                        else:

                            ParseCommand(update);

                            dolog.WriteLog(ParseUpdate.__name__ + ' - ' + json.dumps(update, indent=2));

            else:

                dolog.WriteLog(ParseUpdate.__name__ + ' - ' + json.dumps(data, indent=2));

        else:

            dolog.WriteLog(ParseUpdate.__name__ + ' - ' + "HTTP code != 200.");

#            exit(1);

    else:

        dolog.WriteLog(ParseUpdate.__name__ + ' - ' + str(response) + '  HTTP request failed');

# ParseUpdate END

### ParseCommand function. This fucntion unparses message from the GetUpdate response and try to get command.
def ParseCommand(update):

    message_text = str(update['message']['text']);

    if (message_text[:1] == '/'):
        # /speedtest command
        if (message_text == '/speedtest'):

            update['message']['bot_reply'] = 'Starting SpeedTest';

            SendMessage(update);

            output = lib_dk.runShellCommand("speedtest-cli", "--simple");

            update['message']['bot_reply'] = output['stdout'] + '\n' + output['stderr'];

            SendMessage(update);

            dolog.WriteLog(ParseCommand.__name__ + ' - ' + json.dumps(update, indent=2));

        else:

            update['message']['bot_reply'] = 'Unexpected command: ' + message_text;

            SendMessage(update);

            dolog.WriteLog(ParseCommand.__name__ + ' - ' + json.dumps(update, indent=2));

    else:

        update['message']['bot_reply'] = 'Just a text: ' + message_text;

        SendMessage(update);

        dolog.WriteLog(ParseCommand.__name__ + ' - ' + json.dumps(update, indent=2));

    #SendMessage(update);

# ParseUpdate END

# SendResolve function marks update (message) as resolved.
def SendResolve(update):

    offset = str(update['update_id'] + 1);

    url = 'https://api.telegram.org/bot' + token + '/' + 'getUpdates?offset=' + offset;

    try:

        response = requests.post(url, timeout=(http_timeout, http_timeout_read));

    except requests.exceptions.RequestException as e:

        dolog.WriteLog(SendMessage.__name__ + ' - Message unresolved: ' + str(e));

    else:

        return 0;
# SendMessage END

### Main
while True:

    response = GetUpdate(token);

    ParseUpdate(response);

    time.sleep(3);

# Main END
