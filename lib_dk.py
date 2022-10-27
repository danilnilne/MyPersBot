import subprocess;
import json;
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