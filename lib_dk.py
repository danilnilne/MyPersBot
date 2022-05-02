import subprocess;
import json;
import mariadb;
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

        cmd_result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True)
        #communicate() returns a tuple (stdout_data, stderr_data). The data will be strings if streams were opened in text mode; otherwise, bytes.
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

### dbConnect
# Returns cur - db_cursor pointing to DB
def dbConnect(**kwargs):
    # kwargs - keywords arguments, like:
    # def my_function(**kid)
    #   print("His last name is " + kid["lname"])
    #
    # my_function(fname = "Tobias", lname = "Refsnes")
    # Connect to MariaDB Platform

    # ret = {'returncode': 0,
    #        'db_connect': 'class',
    #        'stderr': 'text'
    #       }
    try:
        db_connect = mariadb.connect(
            user = bot_conf.db_user,
            password = bot_conf.db_password,
            host = bot_conf.db_host,
            port = 3306,
            database = bot_conf.db_name);

        ret = {'returncode': 0, 'stdout': db_connect, 'stderr': ''};

    except mariadb.Error as e:

        ret = {'returncode': 1, 'stdout': '', 'stderr': str(e)}

        return ret;

    return ret;
### dbConnect END

### dbOps
# This function uses ret = {'returncode': X, 'stdout': db_cursor, 'stderr': 'xxxxxx'} from dbConnect(**kwargs)
# Arguments:
# input should be KeyWords: 'field_name' = 'filed_value'
# table_name: Table name where need to INSERT or SELECT
# ops: INSERT or SELECT or DELETE
# Examle: # table_name = 'speedtest', ops = 'INSERT', input = content
def dbOps (**kwargs):

    db_connect = dbConnect()['stdout']

    db_connect.autocommit = False;

    db_cursor = db_connect.cursor();
    # INSERT - add row to the table with Table table_name and data
    db_data = (kwargs['input']['ping'], kwargs['input']['download'], kwargs['input']['upload']);

    if (kwargs['ops'] == "INSERT"):

        try:

            db_cursor.execute ("INSERT INTO speedtest (ping,download,upload) VALUES (?, ?, ?);", db_data);

        except mariadb.Error as e:

            return str(e);

    db_connect.commit();

    db_connect.close();

    return "OKey";

### dbOps END
