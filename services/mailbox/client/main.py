from base64 import b64encode, b64decode
from os import urandom

from api import API


HOST = '127.0.0.1'
PORT = 3113


def test1():
    api = API(HOST, PORT)

    username, password = urandom(8), urandom(8)
    print(f'Username: {b64encode(username).decode()}, Password: {b64encode(password).decode()}')
    print('[+] Register:', api.register(username, password))
    print('[+] Login:', api.login(username, password))
    print('[+] GetUserInfo:', api.get_user_info(username))
    print(api._session.cookies)
    print('[+] Me:', api.me())


def test2():
    dialogue_name = b'Some dialogue'
    api1 = API(HOST, PORT)
    username1, password1 = urandom(8), urandom(8)
    print('[+] Register:', api1.register(username1, password1))
    print('[+] Login:', api1.login(username1, password1))

    api2 = API(HOST, PORT)
    username2, password2 = urandom(8), urandom(8)
    print('[+] Register:', api2.register(username2, password2))
    print('[+] Login:', api2.login(username2, password2))

    print('[+] CreateDialogue:', api1.create_dialogue(username2, dialogue_name))
    dialogue = api1.get_dialogue(username2)['response']['dialogue']
    dialogue_id = b64decode(dialogue['id'].encode())
    print('[+] GetDialogue:', dialogue)

    text = urandom(10)
    msg = api1.send_msg(dialogue_id, text)['response']['msg']
    print('[+] SendMsg:', msg)

    msg1 = api1.get_msg(b64decode(msg['id'].encode()), b64decode(msg['encryption'].encode()))
    print(msg1)

    msg2 = api2.get_msg(b64decode(msg['id'].encode()))
    print(msg2)


if __name__ == '__main__':
    test2()