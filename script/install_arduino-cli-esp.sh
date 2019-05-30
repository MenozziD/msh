cd $HOME
curl https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2 --output arduino-cli.tar.bz2
tar -xaf arduino-cli.tar.bz2
rm -f arduino-cli.tar.bz2
mv arduino-cli-* arduino-cli
mkdir opt
mkdir opt/arduino
curl "https://downloads.arduino.cc/arduino-1.8.9-linuxarm.tar.xz" --output arduino.tar.xz
tar -xvf arduino.tar.xz
sudo mv arduino-*.*/ $HOME/opt/arduino
