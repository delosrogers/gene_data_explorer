import pandas as pd
import platform
from flask_wtf import FlaskForm
from gene_data_explorer import db
from copy import deepcopy
from sqlalchemy import Column, Integer, String 
from wtforms import SubmitField, StringField, SelectField, TextAreaField, BooleanField, validators
#from sqlalchemy.ext.automap impor
from flask_login import UserMixin
# t automap_base

#
#""" class genes(db.Model):
#    __tablename__ = 'genes'
#
#class cco1_jmjd_RNAseq(db.Model):
#    __tablename__ = 'cco1_jmjd_RNAseq'
#
#class Ahringer_RNAi(db.Model):
#    __tablename__ = 'Ahringer_RNAi'
#
#class Vidal_RNAi(db.Model):
#    __tablename__ = 'Vidal_RNAi'
#
#class dat1p_tph1p_v_N2(db.Model):
#    __tablename__ = 'dat1p_tph1p_v_N2'
#
#class dat1p_v_N2(db.Model):
#    __tablename__ = 'dat1p_v_N2'
#
#class eps8_RNAi(db.Model):
#    __tablename__ = 'eps8_RNAi'
#
#class human_genes(db.Model):
#    __tablename__ = 'human_genes'
#
#class human_mito_stress(db.Model):
#    __tablename__ = 'human_mito_stress'
#
#class rab3p_v_N2(db.Model):
#    __tablename__ = 'rab3p_v_N2'
#
#class tph1p_v_N2(db.Model):
#    __tablename__ = 'tph1p_v_N2'

""" class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
 """

class Authorized_user_emails(db.Model):
    __tablename__ = 'authorized_user_emails'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    __table_args__ = {'extend_existing': True} 
    @staticmethod
    def add_email(email):
        print('adding email')
        new_email = Authorized_user_emails(email=email) 
        email_exists = Authorized_user_emails.query.filter(email == email).first()
        if email_exists is None:
            db.session.add(new_email)
            print(new_email, email_exists)
            db.session.commit()
        
    @staticmethod
    def remove_email(email):
        email_db_entry = Authorized_user_emails.query.filter(email == email).first()
        if email_db_entry is not None:
            db.session.delete(email_db_entry)

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(45), unique=False, nullable=False)
    authed = db.Column(db.Boolean(), nullable=False)
    
#    @staticmethod
#    def exists(user_id):
#        user = db.session.query(User).filter(User.id == user_id).first()
#        return user
    @staticmethod
    def get(user_id):
        user = db.session.query(User).filter(User.id == user_id).first()
        return user
    
    def get_id(self):
        return str(self.id)
    
    def create(self):
        db.session.add(self)

    def is_authenticated(self):
        return self.authed

    def is_active(self):
        #for now all authenticated accounts are active
        return self.authed

    @staticmethod
    def authorize_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            print('authorizing')
            print(user)
            user.authed = True
            db.session.commit()

    @staticmethod
    def deauthorize_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            user.authed=False
            db.session.commit()

    @staticmethod
    def get_all_users():
        users = User.query
        print(users.statement)
        df = pd.read_sql(users.statement, db.engine)
        print(df)
        return df
    
    def __repr__(self):
        return "<User(id = {id}, username = {username}, email = {email}, user_type = {user_type}".format(
            id=self.id, username=self.username, email=self.email, user_type=self.user_type
        )

db.Model.prepare(db.engine, reflect=True)
db.create_all()

def join_data(columns: list, tables: list, gene_list: list, additional_params="", return_missing="False", gene_type="WormBaseID") -> pd.DataFrame:
    column_names=deepcopy(columns) #current column list will get converted to ORM objects and I need the strings to name df columns
    for i in range(len(columns)):
        #takes columns which are in table.colname format split them by the dot and then use
        #getattr to turn it into a object.
        temp_list = columns[i].split(".")
        tmp_table = getattr(db.Model.classes, temp_list[0])
        columns[i] = getattr(tmp_table, temp_list[1])
    q = db.session.query(*columns)
    genes = db.Model.classes.genes
    print(type(genes.gid))
    for i in range(len(tables)):
        table = getattr(db.Model.classes, tables[i])
        tables[i] = [table, genes.gid == table.gid]
    
    #outer or inner join:
    if return_missing == "True":
        for join_args in tables:
            q = q.outerjoin(*join_args)
    elif return_missing == "False":
        for join_args in tables:
            q = q.join(*join_args)
        
    translate_genes = {'WormBaseID': genes.WormBaseID, 'GeneName': genes.GeneName, 'sequence': genes.sequence}
    gene_type = translate_genes[gene_type]
    gene_tuple = tuple(gene_list)
    q = q.filter(gene_type.in_(gene_tuple)).order_by(genes.WormBaseID.asc())
    df = pd.read_sql(q.statement, db.session.bind)
    df.columns=column_names
    print(df)
    return df, ""

def get_gene_info(gene):
    
    genes = db.Model.classes.genes
    columns = [genes.WormBaseID]
    columns.append(genes.GeneName)
    q = db.session.query(*columns)
    res = q.filter(genes.WormBaseID == gene).all()
    df = pd.DataFrame.from_records(res, columns=columns)
    return df

class Admin_email_management_form(FlaskForm):
    add_or_remove = SelectField(u'add or remove email', choices=['add', 'remove'])
    email = StringField('email', [validators.DataRequired()])
    submit = SubmitField('submit')




class geneModel:
    
    def __init__(self):
        with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
        if platform.system() == 'Linux':
            self.conn = create_connection('gene_data_mysql', 'web_app', passwd)
        else:
            self.conn = create_connection('localhost', 'web_app', passwd)
        self.cursor = self.conn.cursor(buffered=True)
    
    def join_data(self, columns: list, tables: list, genes: list, additional_params="", return_missing="False", gene_type="WormBaseID") -> pd.DataFrame:
        #set SQL join method based off the return_missing paramaeter
        if return_missing == "True":
            join_method = " LEFT OUTER JOIN "
        elif return_missing == "False":
            join_method= " INNER JOIN "
        sql_q = "SELECT"
        #create the correct amount of column feilds
        for i in range(len(columns)-1):
            sql_q = sql_q + " " + columns[i] + " ,"
        sql_q = sql_q + " " + columns[len(columns)-1] + " FROM genes"
        #create the correct number of join table feilds
        for i in tables:
            sql_q = sql_q + join_method + i + " USING (gid)"
        if genes[0] != '' or len(genes)>1 or additional_params != '' or len(additional_params)>1:
            sql_q = sql_q + " WHERE "

        if genes[0] != '' or len(genes)>1:
            sql_q += "genes.{gene_type} in (".format(gene_type = gene_type)
            for i in range(len(genes)-1):
                sql_q = sql_q + "%s,"
            sql_q = sql_q + " %s)"
        sql_q = sql_q + " " + additional_params +";"
        values = tuple(genes)
        try:
            if (values[0] == '' and len(values) == 1):
                self.cursor.execute(sql_q)
            else:
                print(sql_q, values)
                self.cursor.execute(sql_q, values)
            res = self.cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
            print(self.cursor.statement)
        df = pd.DataFrame(data=res, columns=columns)
        return df, self.cursor.statement



    def get_info(self) -> list:
        self.cursor.execute("SELECT * FROM information_schema.columns WHERE table_schema = 'gene_data';")
        #columns = "TABLE_CATALOG TABLE_SCHEMA _TABLE_NAME COLUMN_NAME ORDINAL_POSITION COLUMN DEFAULT IS_NULLABLE DATA_TYPE CHARACTER_MAXIMUM_LENGTH \
        #    CHARACTER_OCTET_LENGTH NUMERIC_PRECISION NUMERIC_SCALE DATETIME_PRECISION CHARACTER_SET_NAME COLUMN_TYPE COLUMN_KEY EXTRA PRIVILEGES COLUMN_COMMENT \
        #        GENERATION_EXPRESSION SRS_ID".split(" ")
        columns = "TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | ORDINAL_POSITION | COLUMN_DEFAULT | IS_NULLABLE | DATA_TYPE | CHARACTER_MAXIMUM_LENGTH | CHARACTER_OCTET_LENGTH | NUMERIC_PRECISION | NUMERIC_SCALE | DATETIME_PRECISION | CHARACTER_SET_NAME | COLLATION_NAME | COLUMN_TYPE  | COLUMN_KEY | EXTRA | PRIVILEGES | COLUMN_COMMENT | GENERATION_EXPRESSION | SRS_ID".split("|")
        df = pd.DataFrame(data = self.cursor.fetchall(), columns=columns)
        return df
        """ self.cursor.execute("SHOW TABLES;")
        tables = self.cursor.fetchall()
        tables = sql_resources.column_to_list(tables)
        describe_list = []
        for i in tables:
            self.cursor.execute("DESCRIBE %s", (i,))
            res = self.cursor.fetchall()
            columns = self.cursor.execute("")
            describe_list.append(pd.DataFrame(data=res)) """





