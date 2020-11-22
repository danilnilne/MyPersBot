import subprocess
 
args = ["speedtest-cli"];

print ("SpeedTest started...");

process = subprocess.Popen(args, stdout=subprocess.PIPE);

output, error = process.communicate();

print(output);

print(error);

print ("Exit...");

