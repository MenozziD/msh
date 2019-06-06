sudo arduino-cli board listall
sudo arduino-cli compile --fqbn esp8266:esp8266:generic test
usb=`arduino-cli board list | grep tty | awk '{print $1}'`
sudo arduino-cli upload -p $usb --fqbn esp8266:esp8266:generic test
