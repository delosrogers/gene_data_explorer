import mysql.connector
from mysql.connector import Error
import pandas as pd
import openpyxl
with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]


conn = mysql.connector.connect(host='localhost',user='mattias',passwd=passwd,database='gene_data')

def add_genes(series, existing_genes):
    if not(series['WormBase Gene ID'] in existing_genes['WBID']):
        sql_q = "INSERT INTO genes (WormBaseID, GeneName, sequence, source) VALUES (%s,%s,%s,%s);"
        values = (
            series['WormBase Gene ID'],
            series['Public Name'],
            series['Sequence Name'],
            "Raz's list of all genes"
        )
        try:
            cursor.execute(sql_q, values)
        except Error as e:
            print(f"The error '{e}' occurred")

cursor = conn.cursor(buffered=True)
sql_q = "SELECT * from genes;"
cursor.execute(sql_q)
genes = cursor.fetchall()
genes_df = pd.DataFrame(genes, columns="gid WBID GeneName sequence source".split(" "))
raz_genes = pd.read_excel("worm_genes_list-geneID-geneName.xlsx", engine='openpyxl')
print(genes_df)
#raz_genes.apply(add_genes, axis=1,args=(genes_df,))
conn.commit()
cursor.close()
conn.close()
