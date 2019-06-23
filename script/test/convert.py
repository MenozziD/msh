from sys import argv


def main(path):
    path = path + "\\"
    f = open(path + ".coverage", "r")
    cont = f.read()
    f.close()
    cont = cont.replace("/home/pi/server/msh/test/", path + "test\\\\")
    cont = cont.replace("/home/pi/server/msh/module/", path + "module\\\\")
    cont = cont.replace("/home/pi/server/msh/controller/", path + "controller\\\\")
    cont = cont.replace("/home/pi/server/msh/", path)
    f = open(path + ".coverage", "w")
    f.write(cont)
    f.close()


if __name__ == '__main__':
    main(argv[1])
