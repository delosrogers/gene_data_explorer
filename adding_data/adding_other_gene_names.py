import pandas as pd
import json
from sqlalchemy import create_engine, VARCHAR, JSON
from sqlalchemy.dialects import mysql

with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]

engine = create_engine('mysql://mattias:{passwd}@127.0.0.1/gene_data'.format(passwd=passwd))

other_names = pd.read_csv('c_elegans.PRJNA13758.WS279.geneOtherIDs.txt', sep = '\t', names = "WBID live sequence name other".split(" "))
output_df = pd.DataFrame(columns="WormBaseID other_names".split(" "))

def jsonify_other_names(row):
    output_df.loc[row.name, 'WormBaseID'] = row['WBID']
    __other_names_json__ = json.dumps(list(row[['sequence','live', 'other']]))
    output_df.loc[row.name, 'other_names'] = __other_names_json__

other_names.apply(jsonify_other_names, axis=1)
output_df.to_csv("to_add_to_database.csv")
#output_df.to_sql('tmp_other_genes', engine.connect(), if_exists='append', index=False, dtype={'WormBaseID': VARCHAR(45), 'other_names': JSON}, method='multi')
