FROM python:3.9

RUN mkdir -p /scrapyd

WORKDIR /scrapyd

ADD requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 6800

CMD ['scrapyd']