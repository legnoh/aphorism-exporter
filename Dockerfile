FROM selenium/standalone-chromium:latest

USER root
ENV WORKDIR=/usr/src/app
WORKDIR ${WORKDIR}

ENV TZ="Asia/Tokyo"
ENV SE_CHROMEDRIVER="/usr/bin/chromedriver"

RUN apt -y install python3 python3-pip

COPY . ${WORKDIR}

RUN pip3 install --break-system-packages -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "./docker-entrypoint.sh" ]

CMD [ "python3", "./main.py" ]
