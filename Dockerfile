FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

COPY entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]