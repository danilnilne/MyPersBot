import subprocess;
import json;
#import mariadb;
import sys;
import bot_conf;
import time;

### runShellCommand function runs shell command with options and returns
# ret = {'returncode': 0,
#        'stdout': 'text',
#        'stderr': 'text'
#       }
def runShellCommand (*args):

    ret = {};

    try:

        cmd_result = subprocess.Popen(args,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      shell=False,
                                      text=True)
        # communicate() returns a tuple (stdout_data, stderr_data).
        # The data will be strings if streams were opened in text mode; otherwise, bytes.
        ret['stdout'], ret['stderr'] = cmd_result.communicate(timeout=30)

    except OSError as e:

        ret = {'returncode': e.errno, 'stdout': '', 'stderr': e.strerror}

        return ret;

    except subprocess.TimeoutExpired as e:

        ret = {'returncode': 1, 'stdout': e.stdout, 'stderr': "TimeoutExpired"}

        return ret;

    except subprocess.SubprocessError as e:

        ret = {'returncode': 1, 'stdout': '', 'stderr': e}

        return ret;

    ret['returncode'] = 0;

    return ret;
### runShellCommand END

# Connect to MariaDB
def dbConnect():

    try:
        db_connect = mysql.connector.connect(
            user = bot_conf.db_user,
            password = bot_conf.db_password,
            host = bot_conf.db_host,
            port = bot_conf.db_port,
            database = bot_conf.db_name)

        ret = {'returncode': 0, 'stdout': db_connect, 'stderr': ''};

    except mysql.connector.Error as e:

        ret = {'returncode': 1, 'stdout': '', 'stderr': str(e)};

        return ret;

    return ret;

### dbOps: Operations with tables, where db_connect is database connection

# This function uses ret from dbConnect() func:
# {     'returncode': X,
#       'stdout': db_cursor,
#       'stderr': 'xxxxxx'
# }
# Arguments:
# input should be KeyWords: 'field_name' = 'filed_value'
# table_name: Table name where need to INSERT or SELECT
# ops: INSERT or SELECT or DELETE
# Examle: # table_name = 'speedtest', ops = 'INSERT', input = content
def dbOps (**kwargs):

    db_connection_info = dbConnect();

    if db_connection_info['returncode'] == 0:

        db_connect = db_connection_info['stdout']
        db_connect.autocommit = False;
        db_cursor = db_connect.cursor();

        db_output = db_cursor.execute("SELECT id, timestamp, description FROM events");

        row = db_output.fetchone();
        print(*row, sep=' ');

        #return db_output;

    else:

        return db_connection_info['stderr'];

    db_cursor.close();
    db_connect.commit();
    db_connect.close();
### dbOps END
