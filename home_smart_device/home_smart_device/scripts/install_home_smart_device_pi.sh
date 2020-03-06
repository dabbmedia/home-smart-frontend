#!/bin/bash
# install python, pip and python packages
# sudo apt-get install -y python3
sudo apt-get update

sudo apt-get install -y python3-pip

sudo apt-get install -y python3-opencv

# install and configure apache httpd for python
sudo apt-get install -y apache2 libapache2-mod-wsgi-py3

# raspbian only?
# sudo apt-get install -y apache2-utils

sudo usermod -a -G www-data pi

sudo mkdir /var/www/home_smart_device

sudo chown -Rf pi:pi /var/www/home_smart_device

# sudo a2enmod wsgi

# postgres support
# pip3 install psycopg2-binary

# already installed?
# sudo pip3 install numpy

sudo pip3 install Flask

# enable camera
# (for internal pi camera, not USB cams)
# sudo raspi-config
# modprobe bcm2835-v4l2

# enable camera at boot
# sudo vim /etc/rc.local
sudo chmod 0777 /dev/video0

# rotate camera image (for pi cam)
# sudo v4l2-ctl --set-ctrl=rotate=270

# update apache config
# sudo vim /etc/apache2/sites-available/000-default.conf

# transfer files
# scp -r ./home_smart_device/* pi@10.0.0.103:/var/www/home_smart_device/

sudo apachectl restart

