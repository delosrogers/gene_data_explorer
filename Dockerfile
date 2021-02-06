FROM python:3.8
COPY ./gene_data_explorer/requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update
RUN apt-get upgrade -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN apt-get install -y python-mysqldb default-mysql-client npm gcc g++ build-essential unixodbc-dev 
RUN pip install --upgrade pip
RUN pip install -U -r requirements.txt
COPY . /app
WORKDIR /app/gene_data_explorer
RUN npm install .
WORKDIR /app
ENV RUNNING_IN_DOCKER=TRUE
EXPOSE 5000
EXPOSE 80
CMD ./run_flask.sh
#CMD bash

# FROM tiangolo/uwsgi-nginx-flask:python3.8
# COPY ./gene_data_explorer/requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN export FLASK_APP=gene_data_explorer
# COPY . /app