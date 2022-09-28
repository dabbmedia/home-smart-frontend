#!/bin/bash
# install python, pip and python packages
su -

pkg_add python-3.6.6p1
# pkg_add py3-pip-9.0.3
# ln -sf /usr/local/bin/pip3.6 /usr/local/bin/pip

# sudo apt-get install -y python3-opencv
pkg_add opencv-2.4.13.4p0

# install and configure apache httpd for python
pkg_add apache-httpd-2.4.35 apache-httpd-common-2.4.35
pkg_add ap2-mod_wsgi-4.6.4p0 py-wsgiutils-0.7p6

usermod -G www brent

mkdir /var/www/home_smart_device

chown -Rf brent:brent /var/www/home_smart_device

# update apache config
# vim /etc/apache2/extra/httpd-vhosts.conf

# update main apache config
# 1) uncomment virtual host include
# 2) enable mod_rewrite (uncomment)
# 3) enable mod_wsgi (add LoadModule wsgi_module /usr/local/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.so)
# /usr/local/lib/apache2/mod_wsgi.so didn't seem to work
# vim /etc/apache2/httpd2.conf

# enable apache to run at boot
rcctl enable httpd

# sudo a2enmod wsgi
pip install --upgrade pip

# can be used instead of installing mod_wsgi
# with pkg_add
# pip install mod-wsgi

pip3 install opencv-python
# pip install opencv-utils

# postgres support
# pip3 install psycopg2-binary

# already installed?
pip3 install numpy

pkg_add py3-flask-0.12.3p0

chmod 0777 /dev/video0

apachectl restart

