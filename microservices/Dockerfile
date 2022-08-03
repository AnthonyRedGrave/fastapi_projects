FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

ADD app.py app.py

EXPOSE 8081:8081

# RUN python -m pip install requirements.txt