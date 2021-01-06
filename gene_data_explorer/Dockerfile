FROM python:3.8
COPY ./gene_data_explorer/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -U -r requirements.txt
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python-mysqldb default-mysql-client
ENV RUNNING_IN_DOCKER=TRUE
COPY . /app
EXPOSE 5000
CMD ./run_flask.sh
#CMD bash

# FROM tiangolo/uwsgi-nginx-flask:python3.8
# COPY ./gene_data_explorer/requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN export FLASK_APP=gene_data_explorer
# COPY . /app