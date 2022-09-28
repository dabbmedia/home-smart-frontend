#!/bin/bash
# install python, pip and python packages
# sudo apt-get install -y python3
# sudo apt-get update

sudo apt-get install -y gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
  gstreamer1.0-opencv gstreamer1.0-pocketsphinx \
  libgstreamer1.0-0 libgstreamer1.0-0-dbg libgstreamer1.0-dev \
  gstreamer1.0-plugins-rtp \
  gstreamer1.0-rtsp gstreamer1.0-rtsp-dbg \
  gstreamer1.0-omx-rpi gstreamer1.0-omx-rpi-config gstreamer1.0-omx-rpi-dbgsym \
  gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-x \
  gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-pulseaudio \
  libnginx-mod-rtmp
#   nginx-light 
  # gstreamer1.0-omx gstreamer1.0-omx-generic gstreamer1.0-omx-generic-confi \

sudo apt-get install -y python3-pip python3-opencv

# postgres support
# pip3 install psycopg2-binary

# already installed?
# sudo pip3 install numpy

sudo pip3 install Flask

sudo usermod -a -G www-data pi

sudo mkdir /var/www/home_smart_device
sudo chown -Rf pi:pi /var/www/home_smart_device

sudo mkdir /tmp/hls
sudo chown -Rf pi:pi /tmp/hls
sudo chmod -Rf 0770 /tmp/hls

sudo mkdir /tmp/jpg
sudo chown -Rf pi:pi /tmp/jpg
sudo chmod -Rf 0770 /tmp/jpg

# enable camera
# (for internal pi camera, not USB cams)
sudo raspi-config
sudo modprobe bcm2835-v4l2
sudo chmod 0660 /dev/video0
sudo chown pi:video /dev/video0

# configure SSL self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
# create a strong Diffie-Hellman group for negotiating Perfect Forward Secrecy with clients
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

# rotate camera image (for pi cam)
# sudo v4l2-ctl --set-ctrl=rotate=270

# update apache config
# sudo vim /etc/apache2/sites-available/000-default.conf

# transfer files
# scp -r ./home_smart_device/* pi@10.0.0.103:/var/www/home_smart_device/

sudo apachectl restart

