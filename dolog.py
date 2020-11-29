import bot_conf;
import os
import datetime

#CheckFile fuction checks provided path if it exist on the disk
def CheckLogFile(path):

    if os.path.exists(path):

        #print('Path exist: ', path);

        return(0);

    else:

        print('Path does not exist. Creating: ', path);

        path_parts = path.rpartition('/'); # 0: /home/pi/code/tmp/logs; 1: /; 2: bot.log;

        if os.path.exists(path_parts[0]):

            print("Directory exists ", path_parts[0] + '. Creating Log File', path_parts[2]);

            try:

                log_fd = open(path, "a+");

            except:

                print("Unable to create Log File ", path);

                exit(1);

            else:

                print("Log File created.");

                log_fd = open(path, "a+");

                log_fd.write(str(datetime.datetime.now()) + ' - ' + 'Log File created' + '\n');

                log_fd.close();

        else:

            try:

                os.mkdir(path_parts[0]);

            except:

                print("Unable to create parent dir for Log File ", path_parts[0]);

                exit(1);

            else:

                try:

                    log_fd = open(path, "a+");

                except:

                    print("Unable to create Log File ", path);

                    exit(1);

                else:

                    print("Log File created.");

                    log_fd = open(path, "a+");

                    log_fd.write(str(datetime.datetime.now()) + ' - ' + 'Log File created' + '\n');

                    log_fd.close();

#CheckFile END

#WriteLog fuction provide saving log_strings to the log file
def WriteLog (log_string):

    CheckLogFile(bot_conf.log_file);

    log_file = bot_conf.log_file;

    try:

        log_fd = open(log_file, "a+");

    except :

        print("Unable to operate with Log File ", log_file);

        return (1);

    else:

        log_fd.write(str(datetime.datetime.now()) + ' - ' + log_string + '\n');

        log_fd.close();
#WriteLog END

#Main Body

#WriteLog("Hello!");

#Main END;
