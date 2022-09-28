#!/bin/bash
# install python, pip and python packages
sudo apt-get install -y python3

sudo apt-get install -y python3-pip

sudo apt-get install -y python3-opencv

sudo apt-get install -y postgresql-11

sudo apt-get install -y nginx-full

sudo apt-get install -y libnginx-mod-rtmp

# install and configure apache httpd for python
# sudo apt-get install -y apache2

# sudo apt-get install -y libapache2-mod-wsgi-py3

# raspbian only?
# sudo apt-get install -y apache2-utils

sudo mkdir /var/www/home_smart

# sudo a2enmod wsgi

# test uwsgi
# sudo uwsgi --plugin /usr/lib/uwsgi/plugins/python37 -s :0 --ini /var/www/home_smart/home_smart/home_smart.ini
sudo pip3 install uwsgi
sudo touch /var/www/home_smart/home_smart/home_smart.sock
sudo chown pi:www-data /var/www/home_smart/home_smart/home_smart.sock
sudo chmod 0775 /var/www/home_smart/home_smart/home_smart.sock

# postgres support
sudo pip3 install psycopg2-binary

sudo pip3 install numpy

sudo pip3 install Flask

sudo pip3 install opencv-python

sudo pip3 install ffmpeg-python

sudo chmod 0777 /dev/video0

sudo apachectl restart

# disable led
# to /boot/config.txt add the following
# echo -e "\n# disable led\ndtparam=act_led_trigger=none\n" | sudo tee -a /boot/config.txt > /dev/null
printf "\n# disable led for pi zero and picam\ndtparam=act_led_trigger=none\ndisable_camera_led=1" | sudo tee -a /boot/config.txt > /dev/null
# disable led for Pi4
sudo bash -c "echo none > /sys/class/leds/led0/trigger"
sudo bash -c "echo 0 > /sys/class/leds/led0/brightness"
sudo bash -c "echo none > /sys/class/leds/led1/trigger"
sudo bash -c "echo 0 > /sys/class/leds/led1/brightness"

