from string import ascii_letters, digits
from random import choice
from json import loads, dumps
from os import system
from logging import info, exception


def add_user(username, password):
    try:
        letters_and_digits = ascii_letters + digits
        token_string = ''.join(choice(letters_and_digits) for i in range(36))
        data_file = read_file()
        data_json = data_file.split("const Auth = ")[1].split(";")[0]
        data = loads(convert_to_json(data_json))
        usernames = data['usernames']
        max_uid = 0
        for value in usernames.values():
            if int(value) > max_uid:
                max_uid = int(value)
        uid = str(max_uid + 1)
        user = {
            "uid": uid,
            "name": username,
            "password": password,
            "tokens": [token_string]
        }
        token = {
            "uid": uid,
            "accessToken": token_string,
            "refreshToken": token_string,
            "userId": uid
        }
        data['usernames'][username] = uid
        data['users'][uid] = user
        data['tokens'][token_string] = token
        data_json_new = convert_to_file(data)
        write_file(data_file.replace(data_json, data_json_new))
    except Exception:
        exception("Exception")


def delete_user(username):
    try:
        data_file = read_file()
        data_json = data_file.split("const Auth = ")[1].split(";")[0]
        data = loads(convert_to_json(data_json))
        uid = data['usernames'][username]
        del data['usernames'][username]
        token = data['users'][uid]['tokens'][0]
        del data['users'][uid]
        del data['tokens'][token]
        data_json_new = convert_to_file(data)
        write_file(data_file.replace(data_json, data_json_new))
    except Exception:
        exception("Exception")


def update_user(username, password):
    try:
        data_file = read_file()
        data_json = data_file.split("const Auth = ")[1].split(";")[0]
        data = loads(convert_to_json(data_json))
        uid = data['usernames'][username]
        data['users'][uid]['password'] = password
        data_json_new = convert_to_file(data)
        write_file(data_file.replace(data_json, data_json_new))
    except Exception:
        exception("Exception")


def convert_to_json(data_json):
    data_json_new = data_json\
        .replace("clients", "\"clients\"")\
        .replace("clientId", "\"clientId\"") \
        .replace("clientSecret", "\"clientSecret\"") \
        .replace("tokens", "\"tokens\"") \
        .replace("uid", "\"uid\"") \
        .replace("accessToken", "\"accessToken\"") \
        .replace("refreshToken", "\"refreshToken\"") \
        .replace("users", "\"users\"") \
        .replace("userId", "\"userId\"") \
        .replace("password", "\"password\"") \
        .replace("usernames", "\"usernames\"") \
        .replace("name:", "\"name\":") \
        .replace("authcodes", "\"authcodes\"") \
        .replace("type", "\"type\"") \
        .replace("expiresAt", "\"expiresAt\"") \
        .replace("'", "\"")
    return data_json_new


def convert_to_file(data_json):
    data_json_new = dumps(data_json, indent=4)
    data_json_new = data_json_new\
        .replace("\"clients\"", "clients")\
        .replace("\"clientId\"", "clientId") \
        .replace("\"clientSecret\"", "clientSecret") \
        .replace("\"tokens\"", "tokens") \
        .replace("\"uid\"", "uid") \
        .replace("\"accessToken\"", "accessToken") \
        .replace("\"refreshToken\"", "refreshToken", ) \
        .replace("\"users\"", "users") \
        .replace("\"userId\"", "userId") \
        .replace("\"password\"", "password") \
        .replace("\"usernames\"", "usernames") \
        .replace("\"name\":", "name:") \
        .replace("\"authcodes\"", "authcodes", ) \
        .replace("\"type\"", "type") \
        .replace("\"expiresAt\"", "expiresAt") \
        .replace("\"", "'")
    return data_json_new


def read_file():
    f = open('../oauth/datastore.js', 'r')
    data_file = f.read()
    f.close()
    return data_file


def write_file(data_file):
    f = open('../oauth/datastore.js', 'w')
    f.write(data_file)
    f.close()
    cmd = "cd /home/pi/server/oauth && npm restart 1>/dev/null 2>/dev/null &"
    info("Eseguo comando: %s", cmd)
    system(cmd)
