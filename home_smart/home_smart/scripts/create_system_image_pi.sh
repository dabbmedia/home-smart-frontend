#!/bin/bash

# download the raspbian lite image
# https://downloads.raspberrypi.org/raspios_lite_armhf_latest

# copy Raspberry Pi OS into the project, if using a new version
cp ~/Downloads/2020-05-27-raspios-buster-lite-armhf.zip ~/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/
# unzip the image
open /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/2020-05-27-raspios-buster-lite-armhf.zip

# Install the raspberry pi image
# https://www.raspberrypi.org/documentation/installation/installing-images/mac.md
# 
# Determine the SD device
diskutil list
# Insert disk and run again
diskutil list
# unmount disk
diskutil unmountDisk /dev/disk2
# erase/format disk
sudo diskutil eraseDisk FAT32 RPI_OS MBRFormat /dev/disk2
# unmount disk
diskutil unmountDisk /dev/disk2
# write the image
sudo dd bs=1m if=/Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/2020-05-27-raspios-buster-lite-armhf.img of=/dev/rdisk2; sync

# configure networking for the image's instance
## re-insert the disk
# enable ssh for the image instances by 
# copying an empty file named ssh
cp /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/headless/ssh /Volumes/boot/
# configure wireless networking
# currently using static IP, change to DHCP and configure DNSMasq for home_smart domain names
cp /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/headless/wpa_supplicant.conf /Volumes/boot/

echo " ip=10.0.0.105" >> /Volumes/boot/cmdline.txt

# eject disk
diskutil eject /dev/rdisk2
