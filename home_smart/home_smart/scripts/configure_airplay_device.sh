#!/bin/bash

# update the repo cache
sudo apt-get update

sudo apt-get install shairport-sync

# set the BT device name (overrides hostname)
# sudo touch /etc/machine-info
# echo "HomeSmartSoundBar" > sudo /etc/machine-info
# sudo chown bluetooth:bluetooth /etc/machine-info

# sudo usermod -a -G bluetooth pi

# # add/uncomment needed lines
# sudo vi /etc/bluetooth/main.conf
# # Name = HomeSmartSoundBar
# # Class = 0x41C
# # DiscoverableTimeout = 0

# sudo systemctl restart bluetooth

# sudo bluetoothctl
# [bluetooth]# power on
# [bluetooth]# discoverable on
# [bluetooth]# pairable on
# [bluetooth]# agent on
# [bluetooth]# exit

# # disable bluetooth sap plugin
# sudo mkdir /etc/systemd/system/bluetooth.service.d/
# sudo touch /etc/systemd/system/bluetooth.service.d/01-disable-sap-plugin.conf
# echo "[Service]" > sudo /etc/systemd/system/bluetooth.service.d/01-disable-sap-plugin.conf
# echo "ExecStart=" >> sudo /etc/systemd/system/bluetooth.service.d/01-disable-sap-plugin.conf
# echo "ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap" >> sudo /etc/systemd/system/bluetooth.service.d/01-disable-sap-plugin.conf
# # if not rebooting, restart service
# # sudo systemctl daemon-reload
# # sudo systemctl restart bluetooth.service

# sudo reboot

# sudo systemctl status bluetooth
