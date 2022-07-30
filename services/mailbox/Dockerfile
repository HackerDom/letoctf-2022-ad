FROM python:3.10.5-slim

RUN useradd -M -s /bin/false mailbox

RUN mkdir -p /services/mailbox

WORKDIR /services/mailbox

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ .

USER mailbox

CMD [ "gunicorn", "--bind", "0.0.0.0:3113", "--workers", "4", "--worker-connections", "1024", "main:app"]
