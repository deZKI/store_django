FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "/entrypoint.sh"]