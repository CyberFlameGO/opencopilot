import time

import requests


def poll(url: str) -> bool:
    print("polling with url:", url, "...")
    while True:
        if query(url):
            return True
        print(".", end=" ", flush=True)
        time.sleep(3)


def query(url: str) -> bool:
    try:
        result = requests.get(url, timeout=10)
        if result.status_code == 200:
            return True
    except:
        pass
    return False
