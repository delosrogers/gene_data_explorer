import pandas as pd
import json
from sqlalchemy import create_engine, VARCHAR, JSON
from sqlalchemy.dialects import mysql
from pathlib import Path
import numpy as np
import os

global numMissing
numMissing = 0

def replace_empty_genes_with_sequence(row: pd.Series) -> pd.Series:
    if row["GeneName"] == "" or row["GeneName"] == np.nan:
        row["GeneName"] = row["sequence"]
    return row

def add_wb_id(row: pd.Series, genes: pd.DataFrame) -> pd.Series:
    
    if row["sequence"] in genes.index:
        row["WormBaseID"] = genes.loc[row["sequence"], "WormBaseID"]
        if type(row["WormBaseID"]) == pd.Series:
            row["WormBaseID"] = "multiple" + row["WormBaseID"][0] + row["WormBaseID"][1]
    else:
        global numMissing
        numMissing += 1
        #print(row, "missing", numMissing)
        row["WormBaseID"] = "missing" + str(numMissing)
    return row

def make_well_location(row: pd.Series) -> pd.Series:
    row["well"] = str(row["row"]) + str(row["col"])
    return row

passwd = os.getenv("MYSQL_PASSWORD")

engine = create_engine('mysql+pymysql://web_app:{passwd}@127.0.0.1:6603/new_gene_data'.format(passwd=passwd))

genes = pd.read_csv(
    Path('./data/c_elegans.PRJNA13758.WS279.geneIDs.txt'), 
    names=["a number", "WormBaseID", "GeneName", "sequence", "live", "gene_type"])

genes.drop("a number", axis=1)

genes = genes.apply(replace_empty_genes_with_sequence, axis=1)

# genes.to_sql("genes", engine, index=False, index_label="WormBaseID", method="multi")

Ahringer_RNAi = pd.read_csv(
    Path("./data/Ahringer RNAi.csv"),
    names="sequence plate well chrom fwd_primer rev_primer source_bio_science_life_sciences_location extra_info plate_in_supplemental well_in_supplemental grew_in_96_well".split(" "),
    header=0
)
Vidal_RNAi = pd.read_csv(
    Path("./data/Vidal RNAi.csv"),
    names="sequence plate row col vector host antibiotics orf_id_ws9 ws112_size ws9_size chrom start stop".split(" "),
    header=0
)

Ahringer_RNAi = Ahringer_RNAi.apply(add_wb_id, axis=1, args=(genes.set_index("sequence"),))
Vidal_RNAi = Vidal_RNAi.apply(add_wb_id, axis=1, args=(genes.set_index("sequence"),))
Vidal_RNAi = Vidal_RNAi.apply(make_well_location, axis=1)

Ahringer_RNAi.to_sql("Ahringer_RNAi", engine)
Vidal_RNAi.to_sql("Vidal_RNAi", engine)
print(Vidal_RNAi["WormBaseID sequence plate well row col".split(" ")])




