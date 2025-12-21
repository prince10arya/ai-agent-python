FROM python:3.13.5-slim-bullseye

RUN apt-get update && apt-get install -y curl

# //* Create python virtual environment
RUN python3 -m venv /opt/venv/

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

ENV PATH=/opt/venv/bin:$PATH
ENV PYTHONPATH=/app

RUN pip install -r /tmp/requirements.txt

COPY ./src /app

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
