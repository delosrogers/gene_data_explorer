FROM python
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3"]
EXPOSE 5000/tcp
CMD ["app.py"]