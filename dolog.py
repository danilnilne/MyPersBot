import bot_conf;
import os


#CheckFile fuction checks provided path if it exist on the disk
def CheckLogFile(path):

    if os.path.exists(path):

        print('Такой путь существует: ', path);

        return(0);

    else:

        print('Такого пути нет. Создаем...', path);

        path_parts = path.rpartition('/'); # 0: /home/pi/code/tmp/logs; 1: /; 2: bot.log;

        try:

            os.mkdir(path_parts[0]);

        except:

            print("Unable to create dir for log file");

            exit(1);

        else:

            try:

                log_fd = open(path, "a+");

            except:

                print("Unable to create log file.");

                exit(1);

            else:

                print("Log File created.")



#CheckFile END

#WriteLog fuction provide saving log_strings to the log file
def WriteLog (log_string):

    log_file = bot_conf.log_file;

    try:

        log_fd = open(log_file, "a+");

    except :

        print("Unable to operate with log file");

        return (1);

    else:

        print(log_file);
        print(log_string);
    #check if file exits or can be created
    #check if file more than
#WriteLog END

#Main Body

CheckLogFile(bot_conf.log_file);

WriteLog("Hello!");
#Main END;
