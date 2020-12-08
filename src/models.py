import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database='gene_data',
            port=6603,

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection





class geneModel:
    
    def __init__(self):
        with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
        self.conn = create_connection('localhost', 'web_app', passwd)
        self.cursor = self.conn.cursor(buffered=True)
    
    def join_data(self, columns: list, tables: list, genes: list, additional_params="") -> pd.DataFrame:
        sql_q = "SELECT"
        #create the correct amount of column feilds
        for i in range(len(columns)-1):
            sql_q = sql_q + " " + columns[i] + " ,"
        sql_q = sql_q + " " + columns[len(columns)-1] + " FROM genes"
        #create the correct number of join table feilds
        for i in tables:
            sql_q = sql_q + " INNER JOIN "+ i + " USING (gid)"
        sql_q = sql_q + " WHERE genes.WormbaseID IN ("
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
        return df, self.cursor.statement

db = geneModel()


