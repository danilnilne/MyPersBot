import subprocess;
import json;

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

print(runShellCommand("speedtest-cli", "--json", "--share"));
