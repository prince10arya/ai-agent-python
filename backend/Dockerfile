FROM python:3.13.5-slim-bullseye

# //* Create python virtual environment
RUN python3 -m venv /opt/venv/

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

ENV PATH=/opt/venv/bin:$PATH

RUN pip install -r /tmp/requirements.txt

COPY ./src /app



CMD [ "python", "-m", "http.server", "8000"]
