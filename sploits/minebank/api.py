import xmltodict
from gornilo.http_clients import requests_with_retries
import traceback


class API:
    def __init__(self, host: str, port: int):
        self._addr = f'http://{host}:{port}'
        self._session = requests_with_retries()

    def send_request(self, uri, method="get", json=None):
        if method == "get":
            rsp = self._session.get(
                f"{self._addr}{uri}",
                json=json
            )
        elif method == "post":
            rsp = self._session.post(
                f"{self._addr}{uri}",
                json=json
            )
        else:
            raise Exception("Method not found")

        try:
            return rsp.status_code, rsp.json()
        except:
            traceback.print_exc()
            return rsp.status_code, {}

    def signup(self, user, password, ID_number):
        return self.send_request('/signup', "post", json={
                'login': user,
                'password': password,
                'idNumber': ID_number
            })

    def login(self, user, password):
        print(user, password)
        return self.send_request("/signin", "post", json={
                'login': user,
                'password': password
            })

    def logout(self):
        return self.send_request("/logout")

    def get_profile(self):
        return self.send_request("/profile", "get")

    def get_transactions(self):
        return self.send_request("/transaction", "get")

    def create_transaction(self, recipient_account_id: str, diamonds_count: int, description: str):
        return self.send_request("/transaction", "post", json={
            "recipient_accountID": recipient_account_id,
            "diamondsCount": str(diamonds_count),
            "description": description
        })

    def get_transaction_info(self, transaction_id: int):
        xml = f"""<?xml version="1.0" encoding="UTF-8"?><xml><transaction_id>{transaction_id}</transaction_id></xml>"""

        rsp = self._session.post(
            f"{self._addr}/transaction-info",
            headers={'Content-Type': 'application/xml'},
            data=xml
        )
        try:
            return rsp.status_code, xmltodict.parse(rsp.text)["xml"]
        except:
            traceback.print_exc()
            return rsp.status_code, {}
