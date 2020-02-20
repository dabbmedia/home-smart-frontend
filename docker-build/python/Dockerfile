# docker build -t test-python ./docker-build/python
# docker run -it --name test-flask-dev -p 8080:80 test-python bash
# docker run -it --name test-flask-dev -p 80:5000 -v ./home_smart:/var/www/home_smart:rw test-python bash
FROM python:3.7-buster

COPY ./start_flask.sh /var/www/start_flask.sh

RUN apt-get update && apt-get install -y \
        apt-utils \
        locales \
        ##python-opencv \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && pip3 install psycopg2-binary \
    && pip3 install Flask \
    && mkdir /var/www/home_smart

ENV LANG en_US.utf8

CMD [ "/bin/bash", "/var/www/start_flask.sh" ]
EXPOSE 5000
