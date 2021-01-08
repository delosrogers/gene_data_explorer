from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from gene_data_explorer.credentials import *
import os

app = Flask(__name__)

#with open ("./gene_data_explorer/credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
if os.getenv('RUNNING_IN_DOCKER') == 'TRUE':
    host = 'gene_data_mysql'
    port = 3306
else:
    host = '127.0.0.1'
    port = 6603
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://web_app:{passwd}@{host}:{port}/gene_data'.format(passwd = web_app_passwd, host=host, port = port)
db=SQLAlchemy(app)
db.Model = automap_base(db.Model)
db.Model.prepare(db.engine, reflect=True)

import gene_data_explorer.main