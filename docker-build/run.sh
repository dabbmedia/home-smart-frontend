# install python, pip and python packages
apt-get install -y python3

apt-get install -y python3-pip

apt-get install -y python-opencv

# postgres support
# pip3 install psycopg2
pip3 install psycopg2-binary

pip3 install Flask

# install and configure apache httpd for python
apt-get install -y apache2

apt-get install -y libapache2-mod-wsgi-py3

# raspbian only?
# apt-get install -y apache2-utils

# a2enmod wsgi

# apachectl restart
# systemctl restart apache2


# python3 -m venv flask

# source flask/bin/activate


export FLASK_APP=app/home_smart.py
flask run


ffmpeg -f avfoundation -framerate 30 -i "0" -target ntsc-vcd ./test.mpg
