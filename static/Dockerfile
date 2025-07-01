FROM python:3.13.5-slim-bullseye

WORKDIR /app
#RUN mkdir -p /static

# //* same destination
#COPY ./static .
COPY ./src /app

#RUN echo "hello" > index.html

CMD [ "python", "-m", "http.server", "8000"]
