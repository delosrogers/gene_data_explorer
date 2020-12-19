FROM python:3.7
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
EXPOSE 5001/tcp
CMD ["app.py"]