import requests
import schedule
import json
import time
import os
import sys

old_ip = ""
token = ""
try:
    token = os.environ['SERVER_JIANG_TOKEN']
except KeyError:
    print("Please set the environment varibale SERVER_JIANG_TOKEN")
    sys.exit(1)

def notify(text="Hi", desp="winjay"):
    URL = "https://sc.ftqq.com/token={token}.send?text={text}&desp={desp}".format(token=token, text=text, desp=desp)
    try:
        requests.get(URL)
    except requests.exceptions.RequestException as e:
        f = open("logs.txt", "a+")
        f.write(str(e))
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
        set_ip(current_ip)
        notify("ip has changed", current_ip)

def get_old_ip():
    with open("ip.txt", "r") as f:
        return f.read()

def set_ip(ip):
    f = open("ip.txt", "w")
    f.write(ip)
    f.close()

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

