# INSTALL
sudo apt-get install libcppunit-dev libcppunit-1.13-0 uuid-dev pkg-config libncurses5-dev libtool autoconf automake g++ libmicrohttpd-dev libmicrohttpd10 protobuf-compiler libprotobuf-lite10 python-protobuf libprotobuf-dev libprotoc-dev zlib1g-dev bison flex make libftdi-dev libftdi1 libusb-1.0-0-dev liblo-dev libavahi-client-dev python-numpy
sudo apt-get install git
git clone https://github.com/OpenLightingProject/ola.git ola
cd ola
autoreconf -i
 ./configure --enable-rdm-tests CXXFLAGS='-ftrack-macro-expansion=0'

#SCARICO E INSTALLO ARDUINO-CLI
sudo curl "https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2" --output arduino-cli.tar.bz2
sudo tar -xaf arduino-cli.tar.bz2
sudo rm -f arduino-cli.tar.bz2
sudo mv arduino-cli-* /usr/bin/arduino-cli
sudo arduino-cli config init
sudo arduino-cli core update-index
sudo su
echo "proxy_type: auto
sketchbook_path: /root/Arduino
arduino_data: /root/.arduino15
board_manager:
  additional_urls:
    - http://arduino.esp8266.com/stable/package_esp8266com_index.json" >  /root/.arduino15/arduino-cli.yaml
#INSTALLAZIONE CORE SCHEDE
sudo arduino-cli core install esp8266:esp8266
sudo arduino-cli board listall
sudo arduino-cli compile --fqbn esp8266:esp8266:generic test
usb=`arduino-cli board list | grep tty | awk '{print $1}'`
sudo arduino-cli upload -p $usb --fqbn esp8266:esp8266:generic test