#!/usr/bin/env python3.9
import secrets
import time
import traceback

from gornilo import NewChecker, CheckRequest, GetRequest, PutRequest, Verdict

from api import API

checker = NewChecker()
PORT = 1337


def generate_string(length=16) -> str:
    return secrets.token_hex(length)


def generate_creds() -> tuple:
    return generate_string(8), generate_string(), generate_string()


@checker.define_check
def check_service(request: CheckRequest) -> Verdict:
    api = API(request.hostname, PORT)
    username, password, IDnumber = generate_creds()

    status_code, resp_json = api.signup(username, password, IDnumber)
    if status_code != 200:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't register new user")

    status_code, user_profile = api.get_profile()
    if user_profile.get("msg") != "ok" or not user_profile.get("data") \
            or user_profile.get("data").get("login") != username \
            or not user_profile.get("data").get("accountID"):
        print(f"Status code: {status_code}. Response JSON: {user_profile}")
        return Verdict.MUMBLE("Can't get profile")

    transaction_descr = generate_string()
    status_code, resp_json = api.create_transaction(user_profile.get("data").get("accountID"), 1, transaction_descr)
    if status_code != 200:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't create transaction")
    # wait for transaction handle
    time.sleep(1)
    status_code, resp_json = api.get_transactions()
    if status_code != 200 or not resp_json.get("data") \
            or not resp_json.get("data").get("transmitted") \
            or not resp_json.get("data").get("received") \
            or len(resp_json["data"]["received"]) < 1 \
            or not resp_json["data"]["received"][0].get("id"):
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't get transactions")

    transaction_id = resp_json["data"]["received"][0]["id"]
    status_code, resp_json = api.get_transaction_info(transaction_id)
    if status_code != 200 or not resp_json.get("data") \
            or resp_json["data"].get("id") != str(transaction_id) \
            or resp_json["data"].get("sender_accountID") != user_profile.get("data").get("accountID") \
            or resp_json["data"].get("recipient_accountID") != user_profile.get("data").get("accountID") \
            or resp_json["data"].get("status") != "1" \
            or resp_json["data"].get("description") != transaction_descr:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't get transaction info")

    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
def put1(request: PutRequest) -> Verdict:
    r_api = API(request.hostname, PORT)
    r_user, r_pswd, r_id_num = generate_creds()

    t_api = API(request.hostname, PORT)
    t_user, t_pswd, t_id_num = generate_creds()

    status_code, resp_json = r_api.signup(r_user, r_pswd, r_id_num)
    if status_code != 200:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't register new user")

    status_code, resp_json = t_api.signup(t_user, t_pswd, t_id_num)
    if status_code != 200:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't register new user")

    status_code, resp_json = r_api.get_profile()
    if status_code != 200 or not resp_json.get("data") or not resp_json["data"].get("accountID"):
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't get profile")

    r_acc_id = resp_json["data"]["accountID"]

    status_code, resp_json = t_api.create_transaction(r_acc_id, 1, request.flag)
    if status_code != 200 or not resp_json.get("data") or not resp_json["data"].get("transaction_id"):
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't create transaction")

    transaction_id = resp_json["data"]["transaction_id"]
    for _ in range(3):
        status_code, resp_json = r_api.get_transaction_info(transaction_id)
        if status_code == 200 and resp_json.get("data") \
                and resp_json["data"].get("id") == str(transaction_id) \
                and resp_json["data"].get("status") == "1":
            return Verdict.OK(f"{r_user}:{r_pswd}:{transaction_id}")
        time.sleep(1)
    print(f"Status code: {status_code}. Transaction id: {transaction_id}. Response JSON: {resp_json}")
    return Verdict.MUMBLE("Can't get transaction info")


@checker.define_get(vuln_num=1)
def get1(request: GetRequest) -> Verdict:
    r_user, r_pswd, transaction_id = request.flag_id.replace("\n", "").split(":")
    r_api = API(request.hostname, PORT)
    status_code, resp_json = r_api.login(r_user, r_pswd)
    if status_code != 200:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't signin")

    status_code, resp_json = r_api.get_transaction_info(transaction_id)
    if status_code != 200 or not resp_json.get("data"):
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Can't get transaction info")

    if resp_json["data"].get("description") != request.flag:
        print(f"Status code: {status_code}. Response JSON: {resp_json}")
        return Verdict.MUMBLE("Transaction info incorrect")

    return Verdict.OK()


if __name__ == '__main__':
    checker.run()
