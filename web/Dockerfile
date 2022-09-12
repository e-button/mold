FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/www/html/myproject

WORKDIR /var/www/html/myproject

ADD . /var/www/html/myproject

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN chmod +x ./start.sh