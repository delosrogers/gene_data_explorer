import mysql.connector
from mysql.connector import Error
import pandas as pd
import sql_resources
import platform

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database='gene_data',
            port=3306,

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection





class geneModel:
    
    def __init__(self):
        with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
        if platform.system() == 'Linux':
            self.conn = create_connection('gene_data_mysql', 'web_app', passwd)
        else:
            self.conn = create_connection('localhost', 'web_app', passwd)
        self.cursor = self.conn.cursor(buffered=True)
    
    def join_data(self, columns: list, tables: list, genes: list, additional_params="", return_missing="False") -> pd.DataFrame:
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
        #df = self.make_query(sql_q, columns, genes=genes, additional_params=additional_params)
        if genes[0] != '' or len(genes)>1:
            sql_q += "genes.WormBaseID in ("
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

    def make_query(self, sql_q, columns, genes=None, additional_params=""):
        if len(genes)>0:
            sql_q += "genes.WormBaseID in ("
            for i in range(len(genes)-1):
                sql_q = sql_q + "%s,"
            sql_q = sql_q + " %s)"
        sql_q = sql_q + " " + additional_params +";"
        values = tuple(genes)
        try:
            print(sql_q, values)
            self.cursor.execute(sql_q, values)
            res = self.cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
            print(self.cursor.statement)
        df = pd.DataFrame(data=res, columns=columns)
        return df


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





