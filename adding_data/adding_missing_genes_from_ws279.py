import mysql.connector
from mysql.connector import Error
import pandas as pd
import openpyxl
with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]


conn = mysql.connector.connect(host='localhost',user='mattias',passwd=passwd,database='gene_data')

def add_genes(data, existing_genes):
    if not(data['WormBaseID'] in list(existing_genes['WBID'])):
        sql_q = "INSERT INTO genes (WormBaseID, GeneName, sequence, live, type, source) VALUES (%s,%s,%s,%s,%s,%s);"
        values = (
            data['WormBaseID'],
            data['gene_name'],
            data['Sequence_name'],
            data['live'],
            data['type'],
            "WS279 csv of all genes downloaded from ftp site"
        )
        print('inserted{wbid}'.format(wbid = data['WormBaseID']))
        try:
            cursor.execute(sql_q, values)
        except Error as e:
            print(f"The error '{e}' occurred")

cursor = conn.cursor(buffered=True)
sql_q = "SELECT WormBaseID from genes;"
cursor.execute(sql_q)
genes = cursor.fetchall()
genes_df = pd.DataFrame(genes, columns="WBID".split(" "))
sql_q = "SELECT * from tmp_all_gene_ids WHERE gid is null;"
cursor.execute(sql_q)
genes = cursor.fetchall()
genes_to_add = pd.DataFrame(genes, columns="gid unknown WormBaseID gene_name Sequence_name live type".split(" "))
print(genes_df)
genes_to_add.apply(add_genes, axis=1,args=(genes_df,))
conn.commit()
cursor.close()
conn.close()