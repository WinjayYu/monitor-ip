import requests
import schedule
import json
import time
import os
import sys
from datetime import datetime

old_ip = ""
token = ""
try:
    token = os.environ['SERVER_JIANG_TOKEN']
except KeyError:
    print("Please export the environment varibale SERVER_JIANG_TOKEN")
    sys.exit(1)

def notify(text="Hi", desp="winjay"):
    global token
    date = datetime.today().strftime('%Y%m%d %H%M%S')
    URL = "https://sc.ftqq.com/{token}.send?text={text}&desp={desp}".format(token=token, text=text, desp=desp)
    try:
        print(URL)
        res = requests.get(URL)
        f = open("logs.txt", "a+")
        f.write(date + str(res.text) + '\n')
        f.close()
    except requests.exceptions.RequestException as e:
        f = open("logs.txt", "a+")
        f.write(date + str(e))
        f.close()

def job():
    global old_ip
    if not old_ip:
        old_ip = get_old_ip();
    res = requests.get("https://api.ipify.org?format=json")
    ip_json = json.loads(res.text)
    current_ip = ip_json["ip"]
    if old_ip != current_ip:
        old_ip = current_ip
        notify("ipHasChanged", current_ip)
        set_ip(current_ip)
        

def get_old_ip():
    with open("ip.txt", "r") as f:
        return f.read()

def set_ip(ip):
    f = open("ip.txt", "w")
    f.write(ip)
    f.close()

job()
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

