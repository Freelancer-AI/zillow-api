from sys import flags
import requests
from bs4 import BeautifulSoup
from random import choice
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename='/home/ubuntu/flaskapp/app.log', filemode='w', format='%(asctime)s:%(funcName)s():%(lineno)i - %(levelname)s - %(message)s')

headers = {
        'authority': 'www.zillow.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
}

session = requests.Session()
session.headers.update(headers)

proxy = ""

def get_proxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    px = choice(list(map(lambda x:x[0]+':'+x[1] ,zip(map(lambda x:x.text, soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8])))))

    if px.replace('.','').replace(':','').isnumeric():
        return {'https': px}
    else:
        print(f"invalid proxy {px}")  
        return get_proxy()

def proxy_request(req_type, url, **kwargs):
    global proxy
    flag = True
    r = None
    timeout = time.time() + 60*5   # 5 minutes from now
    while 1:
        if time.time() > timeout:
            logging.debug("Request got timeout after 5 min")
            break
        try:
            # first try without proxy
            if flag:
                logging.debug("trying without proxy")
                session.get("https://www.zillow.com", timeout=6)
                r = session.request(req_type, url, timeout=6, **kwargs)
                flag = False
            else :
                logging.debug(f"using proxy {proxy}")
                session.get("https://www.zillow.com", proxies = proxy, timeout=6)
                r = session.request(req_type, url, proxies = proxy, timeout=6, **kwargs)

            if  r.status_code != 200 :
               logging.warning(f"Bad Request: {r.status_code}")
               break

            soup = BeautifulSoup(r.content, 'html.parser')
            mydivs = soup.findAll("div")
            if len(mydivs) > 0:
                if "Captcha" in str(mydivs[0]):
                    logging.warning(f"Captcha error, proxy:{proxy} We have to use diffrent proxy")
                    proxy = get_proxy()
                    continue
            break
        except:
            logging.error(f"Exception occurred: something went wrong!\n{r.content}", exc_info=True)
            break
    return r