FROM python:latest

WORKDIR /app

COPY [ "src/", "." ]
COPY [ "requirements.txt", "." ]
COPY [ "token", "."]
COPY [ "bad", "."]
COPY [ "good", "."]

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
