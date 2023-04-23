FROM python:3.9

RUN apt-get update && apt-get install -y g++

WORKDIR /app

COPY . .

CMD [ "python", "app.py" ]