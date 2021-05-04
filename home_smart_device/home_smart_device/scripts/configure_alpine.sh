#!/bin/bash

# https://wiki.alpinelinux.org/wiki/Raspberry_Pi

# run the install script from Alpine
setup-alpine

# https://wiki.alpinelinux.org/wiki/Raspberry_Pi_-_Headless_Installation
apk add rng-tools
rc-update add rngd boot
rc-update add wpa_supplicant boot
rc-update del networking boot
rc-update -u

# commit changes and reboot
lbu commit -d
reboot