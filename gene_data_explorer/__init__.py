from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from gene_data_explorer.config import *
import os
import urllib

app = Flask(__name__)

#with open ("./gene_data_explorer/credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
if os.getenv('RUNNING_IN_DOCKER') == 'TRUE':
    host = 'gene_data_mysql'
    port = 3306
else:
    host = '127.0.0.1'
    port = os.getenv("MYSQL_PORT", "6603")
db_type = os.getenv("DB_TYPE", "AZURE")
if db_type == "AZURE":
    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'gene-data.database.windows.net'
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWD")
    database = 'gene-data'

    params = urllib.parse.quote_plus(
        'Driver=%s;' % driver +
        'Server=tcp:%s,1433;' % server +
        'Database=%s;' % database +
        'Uid=%s;' % username +
        'Pwd=%s;' % password +
        'Encrypt=yes;' +
        'TrustServerCertificate=no;' +
        'Connection Timeout=30;'
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=' + params
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://web_app:{passwd}@{host}:{port}/gene_data'.format(passwd=MYSQL_PASSWD, host=host, port=port)
db=SQLAlchemy(app)
db.Model = automap_base(db.Model)
db.Model.prepare(db.engine, reflect=True)

import gene_data_explorer.main