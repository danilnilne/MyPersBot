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
    #args = ["speedtest-cli", "--json", "--share"];

    try:

        process = subprocess.Popen(args, stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as e:

        print("Error with Command");

    else:

        output, error = process.communicate();

        return output, error;

### runShellCommand END

### dbConnect
# Returns cur - db_cursor pointing to DB
def dbConnect(**kwargs):
    # kwargs - keywords arguments, like:
    # def my_function(**kid):
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

### MAIN
print(dbConnect());

print(type(dbConnect()));

# print(runShellCommand("speedtest-cli", "--json", "--share"));

### MAIN END
