FROM python:3.10.5-slim

RUN useradd -M -s /bin/false mailbox

RUN mkdir -p /services/mailbox

WORKDIR /services/mailbox

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ .
COPY scripts/ ./scripts

RUN mkdir -p /var/data
RUN chmod +x ./scripts/*

ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD [ "./scripts/run.sh"]
