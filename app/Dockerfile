FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY connection.py /app
COPY crud-rds-mysql.py /app
CMD python crud-rds-mysql.py
