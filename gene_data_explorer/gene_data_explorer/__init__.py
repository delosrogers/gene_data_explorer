from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from gene_data_explorer.credentials import *

app = Flask(__name__)

#with open ("./gene_data_explorer/credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
host = '127.0.0.1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://web_app:{passwd}@{host}:3306/gene_data?auth_plugin=mysql_native_password'.format(passwd = web_app_passwd, host=host)
db=SQLAlchemy(app)
db.Model = automap_base(db.Model)
db.Model.prepare(db.engine, reflect=True)

import gene_data_explorer.main