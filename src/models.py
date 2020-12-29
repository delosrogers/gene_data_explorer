import mysql.connector
from mysql.connector import Error
import pandas as pd
import sql_resources
import platform
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from main import db


class genes(db.Model):
    __tablename__ = 'genes'

class cco1_jmjd_RNAseq(db.Model):
    __tablename__ = 'cco1_jmjd_RNAseq'

class Ahringer_RNAi(db.Model):
    __tablename__ = 'Ahringer_RNAi'

class Vidal_RNAi(db.Model):
    __tablename__ = 'Vidal_RNAi'

class dat1p_tph1p_v_N2(db.Model):
    __tablename__ = 'dat1p_tph1p_v_N2'

class dat1p_v_N2(db.Model):
    __tablename__ = 'dat1p_v_N2'

class eps8_RNAi(db.Model):
    __tablename__ = 'eps8_RNAi'

class human_genes(db.Model):
    __tablename__ = 'human_genes'

class human_mito_stress(db.Model):
    __tablename__ = 'human_mito_stress'

class rab3p_v_N2(db.Model):
    __tablename__ = 'rab3p_v_N2'

class tph1p_v_N2(db.Model):
    __tablename__ = 'tph1p_v_N2'




def join_data(columns: list, tables: list, genes: list, additional_params="", return_missing="False", gene_type="WormBaseID") -> pd.DataFrame:
    q = g.db.session.query(*columns)
    for i in tables:
        i = [i, gene_table.gid == i.gid]
    for join_args in joins:
        q = q.join(*join_args)
    translate_genes = {'WormBaseID': gene_table.WormBaseID, 'GeneName': gene_table.GeneName, 'sequence': gene_table.sequence}
    gene_type = translate_genes[gene_type]
    gene_tuple = tuple(genes)
    q = q.filter(gene_type.in_(gene_tuple)).all()
    df = q.fetchall
    return df, ""


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





