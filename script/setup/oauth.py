from string import ascii_letters, digits
from random import choice


def main():
    token = ''.join(choice(ascii_letters + digits) for i in range(36))
    f = open("token.txt", "w")
    f.write(token)
    f.close()
    client_id = ''.join(choice(ascii_letters + digits) for i in range(32))
    f = open("clientid.txt", "w")
    f.write(client_id)
    f.close()
    client_secret = ''.join(choice(ascii_letters + digits) for i in range(36))
    f = open("clientsecret.txt", "w")
    f.write(client_secret)
    f.close()


if __name__ == '__main__':
    main()
