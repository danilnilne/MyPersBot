import time
import requests;
import bot_conf;
import dolog;
import dbops_events;
import json;
import lib_dk;

token = bot_conf.token;
http_timeout = bot_conf.http_timeout;
http_timeout_read = bot_conf.http_timeout_read;

### GetUpdate function. This fucntion requests updates from tAPI Telegram API.
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
            data = response.json();
            
            if (data['ok'] == True):
                
                try:
                    data['result'];                 
                except:
                
                    dolog.WriteLog(ParseUpdate.__name__ + ' - Incorrect recieved data. There is bad JSON.result');

                else:

                    for update in data['result']:

                        try:

                            update['message'];     # 1 - KeyError: 'message'. There is no message key with value

                        except:
                            
                            dolog.WriteLog(ParseUpdate.__name__ + ' - Incorrect recieved data. There is bad JSON.result[0].message ' + json.dumps(update, indent=2));

                            SendResolve(update);

                        else:

                            ParseCommand(update);

            else:

                dolog.WriteLog(ParseUpdate.__name__ + ' - Incorrect recieved data. There is JSON.ok is not True' + json.dumps(data, indent=2));

        else:

            dolog.WriteLog(ParseUpdate.__name__ + str(response.status_code) + ' - HTTP response code not 200!');

    else:

        dolog.WriteLog(ParseUpdate.__name__ + ' - ' + str(response) + '  HTTP request failed');

# ParseUpdate END

### ParseCommand function. This fucntion unparses message from the GetUpdate response and try to get command.
def ParseCommand(update):

    # Checking Telegram Used ID and username
    try:
        update['message']['from']['id'];
        db_error = dbops_events.dbAdd(update['message']['from']['id']);
    except:
        update['message']['bot_reply'] = "Cannot parse Telegram ID";
        SendMessage(update);

    try:
        update['message']['text']
    except:
        try:
            update['message']['sticker']   # JSON.result[].message.sticker
            
            update['message']['bot_reply'] = 'Stickers are not supported for now!';

            SendMessage(update);
                  
        except:
        
            dolog.WriteLog(ParseCommand.__name__ + ' - Incorrect recieved data. JSON.result[1].message.XXXXXX unknown!' + json.dumps(update, indent=2));
            
            update['message']['bot_reply'] = json.dumps(update['message'], indent=2);
            
            SendMessage(update);

    else:

        message_text = str(update['message']['text']);

        if (message_text[:1] == '/'):

            # SpeedTest command
            if (message_text == '/speedtest'):

                update['message']['bot_reply'] = 'SpeedTest initiated. Waiting for results...';

                SendMessage(update);

                output = lib_dk.runShellCommand("speedtest-cli", "--simple");

                update['message']['bot_reply'] = output['stdout'] + output['stderr'];

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

# ParseCommand END

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
# SendResolve END

### Main
while True:

    response = GetUpdate(token);

    ParseUpdate(response);

    time.sleep(3);

# Main END
