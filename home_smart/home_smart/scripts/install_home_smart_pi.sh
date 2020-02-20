#!/bin/bash
# install python, pip and python packages
sudo apt-get install -y python3

sudo apt-get install -y python3-pip

sudo apt-get install -y python3-opencv

sudo apt-get install -y postgresql-11

# install and configure apache httpd for python
sudo apt-get install -y apache2

sudo apt-get install -y libapache2-mod-wsgi-py3

# raspbian only?
sudo apt-get install -y apache2-utils

sudo mkdir /var/www/home_smart

sudo a2enmod wsgi

# postgres support
sudo pip3 install psycopg2-binary

sudo pip3 install numpy

sudo pip3 install Flask

sudo chmod 0777 /dev/video0

sudo apachectl restart
