import requests;
import conf;


url = 'https://api.telegram.org/bot' + conf.token + '/';

response = requests.get(url + 'getUpdates');

last_update = 0;

if (response.status_code == 200):

	data = response.json();

	try:

		data['result'];

	except Exception:

		print ("No updates...Exit");

	else:

		print(data);

		for update in data['result']:

			print ("--- By Item ---");

			print (update['update_id']);


			if ( int(update['update_id']) > last_update):

				last_update = int(update['update_id']);

		print ("Last update is: " + str(last_update));

else:

	print("HTTP request hasn't code 200!");
