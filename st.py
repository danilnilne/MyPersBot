import subprocess
 
args = ["speedtest-cli"];

process = subprocess.Popen(args, stdout=subprocess.PIPE);

data = process.communicate();

print(data);
