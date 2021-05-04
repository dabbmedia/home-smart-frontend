#!/bin/bash

# connect to the pi after first boot
ssh pi@raspberrypi.local

# update the host name in /etc/hosts
echo "127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1               HomeSmartLightBar" > ~/hosts.txt

sudo cp ~/hosts.txt /etc/hosts

# set the static IP
echo "static ip_address=10.0.0.105/24
static routers=10.0.0.1" > /etc/dhcpcd.conf

# generate host name
# echo "HomeSmartLightBar" > sudo /etc/hostname
sudo hostnamectl set-hostname HomeSmartLightBar

sudo reboot

ssh pi@HomeSmartLightBar.local
