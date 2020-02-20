#!/bin/bash
# install python, pip and python packages
# sudo apt-get install -y python3

sudo apt-get install -y python3-pip

sudo apt-get install -y python3-opencv

# install and configure apache httpd for python
sudo apt-get install -y apache2

sudo apt-get install -y libapache2-mod-wsgi-py3

# raspbian only?
sudo apt-get install -y apache2-utils

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
sudo raspi-config

# enable camera at boot
# sudo vim /etc/rc.local
modprobe bcm2835-v4l2
chmod 0777 /dev/video0

# update apache config
# sudo vim /etc/apache2/sites-available/000-default.conf

sudo apachectl restart

