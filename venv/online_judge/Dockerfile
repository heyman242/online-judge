FROM gcc:latest

RUN apt-get update && apt-get install -y python3

COPY judge/app.py /app/

WORKDIR /app/

CMD [ "python3", "app.py" ]