import requests;

url = 'https://api.telegram.org/bot303397280:AAH9ciWTZt2ZqG7qfJqshZqMUeKW89bRh1o/';

response = requests.get(url + 'getUpdates');

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

			print (update['message']['chat']);

else:

	print("HTTP request hasn't code 200!");


