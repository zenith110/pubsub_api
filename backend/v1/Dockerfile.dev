# set base image (host OS)
FROM python:3.7.9-slim

ENV FLASK_DEBUG=1
ENV prod=False
# set the working directory in the container
WORKDIR /home/backend/app

# copy the content of the local src directory to the working directory
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
RUN pwd
CMD [ "python", "./app.py" ]