FROM python:latest

WORKDIR /app

COPY [ "src/", "." ]
COPY [ "requirements.txt", "." ]
COPY [ "token", "."]
COPY [ "bad", "."]
COPY [ "good", "."]

RUN pip install -r requirements.txt
RUN mkdir db_discordhort

CMD [ "python", "main.py" ]
