import configparser
import requests
import hashlib
import bot_conf

# Variables
ip_addr = bot_conf.router_fqdn
login = bot_conf.login
passw = bot_conf.passw

cookies_current = None
session = requests.session()                            # заводим сессию глобально чтобы отрабатывались куки

def keen_auth(login, passw):                            # авторизация на роутере
   
        response = keen_request(ip_addr, "auth");
            
        if response.status_code == 401:
            md5 = login + ":" + response.headers["X-NDM-Realm"] + ":" + passw
            md5 = hashlib.md5(md5.encode('utf-8'))
            sha = response.headers["X-NDM-Challenge"] + md5.hexdigest()
            sha = hashlib.sha256(sha.encode('utf-8'))
            response = keen_request(ip_addr, "auth", {"login": login, "password": sha.hexdigest()})
            
            if response.status_code == 200:
                
                return True

            else:
            
                return False
    
def keen_request(ip_addr, query, post = None):          # отправка запросов на роутер

    global session

# конструируем url
    url = "http://" + ip_addr + "/" + query

# если есть данные для запроса POST, делаем POST, иначе GET
    if post:
        return session.post(url, json=post)
    else:
        return session.get(url)

# тестируем
# controlPanel/devicesList
# rci/show/interface/WifiMaster0

if keen_auth(login, passw):
	response = keen_request(ip_addr, 'rci/interface/L2TP0/up');

	print(response.text)
