#!/bin/bash

### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# std installation worked for pi zero w, but not headless
# 
# Alpine would install on the RPi 4, but 
# only displayed a red, green, yellow and blue screen
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Alpine R Pi installation instructions
# https://wiki.alpinelinux.org/wiki/Raspberry_Pi

# download the alpine image
# http://alpinelinux.org/downloads/

# copy Raspberry Pi OS into the project, if using a new version
cp ~/Downloads/alpine-rpi-3.12.0-armhf.tar.gz ~/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/
# unzip the image
open /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/alpine-rpi-3.12.0-armhf.tar.gz

# Install the raspberry pi image
# https://www.raspberrypi.org/documentation/installation/installing-images/mac.md
# 
# Determine the SD device
diskutil list
# Insert disk and run again
diskutil list
# unmount disk
diskutil unmountDisk /dev/disk2
# create a FAT32 partition on the disk
# sudo diskutil partitionDisk /dev/disk2 1 MBR "Free Space" "%MS-DOS (FAT32)%" 100%
sudo diskutil eraseDisk FAT32 ALPINE_RPI MBRFormat /dev/disk2
# mount the partition
diskutil mountDisk /dev/disk2

# extract Alpine tarball contents to the disk
cp -Rf /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/alpine-rpi-3.12.0-armhf/* /Volumes/ALPINE_RPI
# copy rpi config/bios file (no options currently needed)
# cp -f /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/usercfg.txt /Volumes/ALPINE_RPI

# configure wifi, ssh and hostname for the image's instance
# https://wiki.alpinelinux.org/wiki/Raspberry_Pi_-_Headless_Installation
cp /Users/brent/Projects/Sites/home_smart/smart_app/vendor/raspberrypi/headless_alpine/localhost.apkovl.tar.gz /Volumes/ALPINE_RPI

# eject disk
sudo diskutil eject /dev/rdisk2

# default user is root (no pass)
