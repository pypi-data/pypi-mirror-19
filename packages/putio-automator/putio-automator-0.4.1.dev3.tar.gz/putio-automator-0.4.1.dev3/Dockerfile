FROM debian:jessie-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential python2.7 python2.7-dev python-pip supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p \
        /app/logs /app/run \
        /files/incomplete /files/downloads /files/torrents \
    && touch /app/run/app.db \
    && chown -R www-data /app/logs /app/run /files

COPY . /app/src/

RUN cd /app/src \
    && python setup.py install

COPY etc/supervisor /etc/supervisor/
COPY etc/config.py /app/src/

EXPOSE 9001
VOLUME ["/files/incomplete", "/files/downloads", "/files/torrents"]
ENTRYPOINT [ "supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf", "--logfile", "/dev/stdout", "--logfile_maxbytes", "0" ]
CMD [ "bash" ]
