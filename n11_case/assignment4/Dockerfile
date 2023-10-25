FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src/producer.py producer.py
COPY src/consumer.py consumer.py
COPY src/dashboard.py dashboard.py
COPY src/templates/ templates/

CMD ["sh", "-c", "python producer.py & python consumer.py & python dashboard.py"]
