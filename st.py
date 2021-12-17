import subprocess;
import json;

args = ["speedtest-cli", "--json", "--share"];

#print ("SpeedTest started...");

try:

    process = subprocess.Popen(args, stdout=subprocess.PIPE)

except subprocess.CalledProcessError as e:

    print("Error with Command");

else:

    output, error = process.communicate();

    #print(output);

    in_json = output;

    parsed_json = json.loads(in_json);

    print(json.dumps(parsed_json, indent=4, sort_keys=True))

    print(error);

    print ("Exit...");
