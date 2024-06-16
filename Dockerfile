FROM python:3.11.4-slim-buster

COPY requirements.txt .

RUN pip install --user -r requirements.txt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . . 

CMD ["python3", "bot/bot.py"]