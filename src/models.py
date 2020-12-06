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
        with open ("./src/credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
        self.conn = create_connection('localhost', 'web_app', passwd)
        self.cursor = self.conn.cursor(buffered=True)
    
    def join_data(self, columns: list, tables: list, genes: list) -> pd.DataFrame:
        tables = tables[1:len(tables)] #remove first entry of tables which is genes because it is implied and messes up parsing
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
        sql_q = sql_q + " %s);"
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

db = geneModel()

print(db.join_data(['genes.WormBaseID', 'tph1p_v_N2.log2FoldChange', 'dat1p_v_N2.log2FoldChange'],['genes', 'tph1p_v_N2', 'dat1p_v_N2'], ['WBGene00000001', 'WBGene00000002']))
#SELECT genes.WormBaseID, tph1p_v_N2.log2FoldChange, dat1p_v_N2.log2FoldChange FROM genes INNER JOIN tph1p_v_N2 USING (gid) INNER JOIN dat1p_v_N2 USING (gid) WHERE genes.WormBaseID IN ('WBGene00000001', 'WBGene00000002');