from os import system


def main():
    system("sudo curl https://codeload.github.com/VanMenoz92/msh/zip/master --output ../msh.zip 1>/dev/null")
    system("sudo curl https://raw.githubusercontent.com/VanMenoz92/msh/master/script/deploy/update_raspberry.sh --output ../update_raspberry.sh 1>/dev/null")
    system("sudo chmod 744 ../update_raspberry.sh")
    system("cd .. && sudo ./update_raspberry.sh")


if __name__ == '__main__':
    main()
