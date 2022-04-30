import subprocess;
import json;
import mariadb;
import sys;
import bot_conf;
import time;

### runShellCommand function runs shell command with options and returns
# output - command' result
# error - possible errors
def runShellCommand (*args):

    # ret = {'returncode': 0,
    #        'stdout': 'text',
    #        'stderr': 'text'
    #       }
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

    error = "none";
    try:
        conn = mariadb.connect(
            user = bot_conf.db_user,
            password = bot_conf.db_password,
            host = bot_conf.db_host,
            port = 3306,
            database=bot_conf.db_name);

        cur = conn.cursor()

    except mariadb.Error as e:

        error = "Error connecting to MariaDB Platform: " + str(e);

        return error;

    return error, cur;

### dbConnect END
