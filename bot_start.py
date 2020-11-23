import time
import requests;
import bot_conf;


token = bot_conf.token;

### GetUpdate function. This fucntion request updates from TAPI.
def GetUpdate(token):

    url = 'https://api.telegram.org/bot' + token + '/' + 'getUpdates';

    response = requests.get(url);

    return response;
# GetUpdate END

### SendMessage function. This fucntion sends data to the chat using TAPI.
def SendMessage(token, update):


    chat_id = str(update['message']['chat']['id']);

    message = str(update['message']['text']);

    #https://api.telegram.org/bot[BOT_API_KEY]/sendMessage?chat_id=[MY_CHANNEL_NAME]&text=[MY_MESSAGE_TEXT]
    url = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&text=' + message;

    print(url);

    #Send Message to the chat
    try:

        response = requests.post(url);

    except:

        print ("Problems with POST request during Send Message to the chat.");

    else:

        #Mark Update as resolved

        offset = str(update['update_id'] + 1);

        url = 'https://api.telegram.org/bot' + token + '/' + 'getUpdates?offset=' + offset;

        try:

            response = requests.post(url);

        except:

            print ("Problems with POST request Mark Update as resolved.");

        else:

            return 0;

# SendMessage END

### ParseUpdate function. This fucntion unparse values from the GetUpdate response.
def ParseUpdate(response):

    if (response.status_code == 200):

        http_code = 200;

#        print ("HTTP Code is 200. Good connection..."); # Debug logging to the console.

        data = response.json();

        try:

            data['result'];

        except:

            print ("No updates. Continue GetUpdates");

        else:

#            print(data);           # Debug logging to the console.

            for update in data['result']:

                ParseCommand(update);

#                print('=====================')
#                print ("The Update: ", update['update_id']);
#                print ("The Message: ", update['message']);
#                print ("The Message.Chat.ID: ", update['message']['chat']['id']);
#                print ("The Message.Chat.ID.Text: ", update['message']['text']);

    else:

        print("HTTP request hasn't code 200!");

        exit(1);
# ParseUpdate END

### ParseCommand function. This fucntion unparse values from the GetUpdate response.
def ParseCommand(update):

#     print ('*=====================*')
#     print ("The Update: ", update['update_id']);
#     print ("The Message: ", update['message']);
#     print ("The Message.Chat.ID: ", update['message']['chat']['id']);
#     print ("The Message.Chat.ID.Text: ", update['message']['text']);
     SendMessage(token, update)
# ParseUpdate END

### Main
while True:

    response = GetUpdate(token);

    ParseUpdate(response);

    time.sleep(3);

# Main END
