# to test:
# docker build -t test-python-apache-wsgi ./docker-build/debian
# docker run -it --name test-flask -p 8080:80 test-python-apache-wsgi bash
FROM httpd:2.4.41

COPY ./apache2.conf /usr/local/apache2/conf/apache2.conf

#COPY ./httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf

#COPY ./index.html /var/www/home_smart/index.html

#COPY ./start_flask.sh /var/www/start_flask.sh

RUN apt-get update && apt-get install -y \
        apt-utils \
        locales \
        python3 \
        python3-pip \
        #python-opencv \
        libapache2-mod-wsgi-py3 \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && pip3 install psycopg2-binary && pip3 install Flask \
    #&& mkdir /var/www/home_smart \
    #&& rm /etc/apache2/sites-enabled/000-default.conf \
    #&& rm -f /etc/apache2/sites-available/000-default.conf \
    && mv /usr/lib/apache2/modules/mod_wsgi.so /usr/local/apache2/modules/mod_wsgi.so \
    && apachectl restart

ENV LANG en_US.utf8