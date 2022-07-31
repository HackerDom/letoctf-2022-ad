FROM python:3.10.5-slim

RUN useradd -M -s /bin/false mailbox

RUN mkdir -p /services/mailbox

WORKDIR /services/mailbox

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ .
COPY scripts/ .

RUN mkdir -p /var/data
RUN chmod +x ./*.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD [ "./run.sh"]
