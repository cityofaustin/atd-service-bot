FROM python:3.8-slim

# Copy our own application
WORKDIR /app
COPY . /app/atd-service-bot

RUN chmod -R 777 /app/atd-service-bot

# # Proceed to install the requirements...do
RUN cd /app/atd-service-bot && apt-get update && \
    pip install -r requirements.txt