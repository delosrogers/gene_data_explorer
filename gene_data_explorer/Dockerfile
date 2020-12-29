FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN export FLASK_APP=gene_data_explorer
COPY . /app