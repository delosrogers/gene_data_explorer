import pandas as pd
import platform
from flask_wtf import FlaskForm
from gene_data_explorer import db
from copy import deepcopy
from sqlalchemy import Column, Integer, String, or_, and_
from wtforms import SubmitField, StringField, SelectField, TextAreaField, BooleanField, validators
from flask_login import UserMixin


class Authorized_user_emails(db.Model):
    __tablename__ = 'authorized_user_emails'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_email(email):
        print('adding email')
        new_email = Authorized_user_emails(email=email)
        email_exists = Authorized_user_emails.query.filter_by(
            email=email).first()
        print('authorized_user_emails add email', new_email, email_exists)
        if email_exists is None:
            db.session.add(new_email)
            print(new_email, email_exists)
            db.session.commit()

    @staticmethod
    def remove_email(email):
        email_db_entry = Authorized_user_emails.query.filter(
            email == email).first()
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
        db.session.commit()

    def is_authenticated(self):
        return self.authed

    def is_active(self):
        # for now all authenticated accounts are active
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
            user.authed = False
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


def join_data(columns: list, tables: list, gene_list: list, return_missing="False", gene_type="WormBaseID") -> pd.DataFrame:
    "take a list of columns tables which they are in and a gene list and make a sql query using sqlalchemy and return a dataframe of the results"
    # current column list will get converted to ORM objects and I need the strings to name df columns
    column_names = deepcopy(columns)
    for i in range(len(columns)):
        # takes columns which are in table.colname format split them by the dot and then use
        # getattr to turn it into a object.
        temp_list = columns[i].split(".")
        tmp_table = getattr(db.Model.classes, temp_list[0])
        columns[i] = getattr(tmp_table, temp_list[1])
    q = db.session.query(*columns)
    genes = db.Model.classes.genes
    print(type(genes.gid))
    for i in range(len(tables)):
        table = getattr(db.Model.classes, tables[i])
        tables[i] = [table, genes.gid == table.gid]

    # outer or inner join:
    if return_missing == "True":
        for join_args in tables:
            q = q.outerjoin(*join_args)
    elif return_missing == "False":
        for join_args in tables:
            q = q.join(*join_args)

    # turn gene type strings into ORM objects that relate to db columns
    translate_genes = {
        'WormBaseID': genes.WormBaseID,
        'GeneName': genes.GeneName,
        'sequence': genes.sequence,
    }
    gene_type = translate_genes[gene_type]
    gene_tuple = tuple(gene_list)
    q = q.filter(gene_type.in_(gene_tuple)).filter(genes.live == "Live").order_by(genes.WormBaseID.asc())
    res = q.all()
    df = pd.DataFrame.from_records(res)
    df.columns = column_names
    print(df)
    return df, q.statement


def get_gene_info(gene):
    """Once gene annotations are added to the database 
        this fuction will return annotations about the given gene"""
    genes = db.Model.classes.genes
    columns = [genes.WormBaseID]
    columns.append(genes.GeneName)
    q = db.session.query(*columns)
    res = q.filter(genes.WormBaseID == gene).all()
    df = pd.DataFrame.from_records(res, columns=columns)
    return df


class Admin_email_management_form(FlaskForm):
    """ wtforms class for adding and removing authorized users """
    add_or_remove = SelectField(
        u'add or remove email', choices=['add', 'remove']
    )
    email = StringField('email', [validators.DataRequired()])
    submit = SubmitField('submit')


def get_db_info() -> pd.DataFrame:
    """ retrieves a dataframe of all tables and columns in the database """
    columns = """TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME |
         ORDINAL_POSITION | COLUMN_DEFAULT | IS_NULLABLE | DATA_TYPE |
         CHARACTER_MAXIMUM_LENGTH | CHARACTER_OCTET_LENGTH | NUMERIC_PRECISION |
         NUMERIC_SCALE | DATETIME_PRECISION | CHARACTER_SET_NAME | COLLATION_NAME |
         COLUMN_TYPE  | COLUMN_KEY | EXTRA | PRIVILEGES | COLUMN_COMMENT |
         GENERATION_EXPRESSION | SRS_ID""".split("|")
    df = pd.read_sql("SELECT * FROM information_schema.columns WHERE table_schema = 'gene_data';",
                     db.engine)
    df.columns = columns
    return df


def get_gene_table() -> pd.DataFrame:
    sql_q = "SELECT * FROM genes;"
    df = pd.read_sql(sql_q, db.session.bind)
    return df

def upload_df(df: pd.DataFrame, name: str) -> pd.DataFrame:
    atributes_dict = {}
