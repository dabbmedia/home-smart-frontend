# to test:
# docker build -t test-nginx ./docker-build/nginx
# docker run -it --name test-flask-uwsgi -p 8080:80 test-nginx bash
FROM nginx:1.16

COPY ./nginx.conf /etc/nginx/nginx.conf

#COPY ./start_uwsgi.sh /usr/share/start_uwsgi.sh

RUN apt-get update && apt-get install -y \
        apt-utils \
        locales \
        python3 \
        python3-pip \
        #python-opencv \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && pip3 install uwsgi && pip3 install psycopg2-binary && pip3 install Flask

ENV LANG en_US.utf8