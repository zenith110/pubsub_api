# set base image (host OS)
FROM python:3.7.9-slim

ENV FLASK_DEBUG=1
# set the working directory in the container
WORKDIR /home/backend/app

RUN apt-get update
RUN apt-get -y install gcc

# copy the content of the local src directory to the working directory
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_DEBUG 1
CMD [ "python", "./app.py" ]