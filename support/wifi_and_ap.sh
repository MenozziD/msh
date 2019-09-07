sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install hostapd -y
sudo apt-get install dnsmasq -y
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
# AGGIUNGI A RC LCOAL
echo 'Add to /etc/rc.local:
service hostapd stop
service dnsmasq stop
iw dev wlan0 interface add uap0 type __ap
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
ifdown wlan0
ip link set uap0 up
ip addr add 192.168.0.1/24 broadcast 192.168.0.255 dev uap0
service hostapd start
ifup wlan0
service dnsmasq start'
read -p "Premere invio per editare il file"
sudo nano /etc/rc.local
# SPOSTO CONFIG ORIGINALI DI DNSMASQ
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
# CREO NUOVE CONFIG DI DNSMASQ
echo 'Add to /etc/hostapd/hostapd.conf:
interface=uap0
dhcp-range=192.168.0.11,192.168.0.30,255.255.255.0,24h'
read -p "Premere invio per editare il file"
sudo nano /etc/dnsmasq.conf
# CREO FILE /etc/hostapd/hostapd.conf
echo 'Add to/etc/hostapd/hostapd.conf:
interface=uap0
driver=nl80211
ssid=Raspberry
country_code=IT
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=c.ronaldo#7
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP'
read -p "Premere invio per editare il file"
sudo nano /etc/hostapd/hostapd.conf
# RIMUOVO COMMENTO A DAEMON_CONF IN /etc/default/hostapd
echo "Set DAEMON_CONF=\"/etc/hostapd/hostapd.conf\" in /etc/default/hostapd"
read -p "Premere invio per editare il file"
sudo nano /etc/default/hostapd
# RIMUOVO COMMENTO net.ipv4.ip_forward=1 IN /etc/sysctl.conf
echo "Set net.ipv4.ip_forward=1 in /etc/sysctl.conf"
read -p "Premere invio per editare il file"
sudo nano /etc/sysctl.conf
# SETTO SERVIZI E RESTART
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo reboot


