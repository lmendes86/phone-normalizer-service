FROM python:3.12-slim

MAINTAINER lmendes86 "lucasam86@gmail.com"
WORKDIR /app

RUN apt update && \
	apt upgrade -y && \
	apt install -y \
	nginx \
	supervisor \
	gcc \
	sqlite3 && \
	apt-get purge -y --auto-remove && \
    rm -rf /var/lib/apt/lists/*

# Nginx
RUN rm -rf /etc/nginx/conf.d/*
COPY conf/nginx.conf /etc/nginx/
COPY conf/ng_server.conf /etc/nginx/conf.d/

COPY app /app/
COPY env/phone_normalizer_service/requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# Supervisor profiles
COPY conf/supervisor_services/* /etc/supervisor/conf.d/

RUN python3 /app/src/phone_normalizer_service/manage.py migrate
COPY db/dump_data.tar.gz /app/
RUN tar -xf dump_data.tar.gz
RUN rm dump_data.tar.gz
RUN python3 /app/src/phone_normalizer_service/manage.py loaddata dump_data.json
RUN rm dump_data.json

EXPOSE 80/tcp

CMD ["/usr/bin/supervisord"]
