FROM python:3.8-slim

WORKDIR /app

COPY . /app
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python transfer_source_tables.py && python coupon_data_processor.py && python coupon_usage_processor.py"]
