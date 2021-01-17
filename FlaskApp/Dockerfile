FROM python:3.7-alpine

WORKDIR /FlaskApp

ENV FLASK_APP=index.py FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run"]