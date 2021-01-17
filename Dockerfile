FROM debian:buster

RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
    ;

ENV APP_ROOT /app
WORKDIR $APP_ROOT
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "/app/shortwave.py"]