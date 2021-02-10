import sys
sys.path.append('/mnt/c/Users/Mattias/Documents/coding/gene_data_explorer')
#import gene_data_explorer.upload_data as upload_data
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import os
import urllib
import threading
from multiprocessing import Process


# driver = '{ODBC Driver 17 for SQL Server}'
# server = 'gene-data.database.windows.net'
# username = os.getenv("AZURE_SQL_USERNAME")
# password = os.getenv("AZURE_SQL_PASSWD")
# database = 'gene-data'

# params = urllib.parse.quote_plus(
#     'Driver=%s;' % driver +
#     'Server=tcp:%s,1433;' % server +
#     'Database=%s;' % database +
#     'Uid=%s;' % username +
#     'Pwd={%s};' % password +
#     'schema=gene_data'
#     'Encrypt=yes;' +
#     'TrustServerCertificate=no;' +
#     'Connection Timeout=30;'
# )

# create_engine('mssql+pyodbc:///?odbc_connect=' + params)

def transform_upload(column_mapper: dict, df: pd.DataFrame) -> pd.DataFrame:
    """ takes a dictionary that maps column names to DESEQ column names
    and transforms the passed in data into DESEQ formatted data
    """
    requiredColumns = ["WormBaseID","baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj"]
    df = df.rename(column_mapper, axis=1)
    existingColumns = list(df.columns)
    columnsToDrop = filter(lambda x: x not in requiredColumns, existingColumns)
    df = df.drop(columnsToDrop, axis=1)
    for i in requiredColumns:
        if i not in existingColumns:
            df[i] = None
    df = df[requiredColumns]
    return df


def add_log_2_fold_change(row: pd.Series, fc_col: str) -> pd.Series:
    if row[fc_col] > 0:
        row["log2FoldChange"] = np.log2(row[fc_col])
    else:
        row["log2FoldChange"] = - np.log2(abs(row[fc_col]))
    return row

def analyze_L4():
    act_raw = pd.read_excel('./data/N2 L4 vs. act1 L4 all differentials.xlsx')
    act_raw = act_raw.apply(add_log_2_fold_change, axis=1, args=("EDGE test: N2 L4 vs act1 L4, tagwise dispersions - Fold change",))

    column_mapper = {
        "Feature ID": "WormBaseID",
        "log2FoldChange": "log2FoldChange",
        "EDGE test: N2 L4 vs act1 L4, tagwise dispersions - P-value": "pvalue",
        "EDGE test: N2 L4 vs act1 L4, tagwise dispersions - FDR p-value correction": "padj",
    }

    act_restructured = transform_upload(column_mapper, act_raw)
    act_restructured.to_csv("./data/restructured_act_L4.csv")

def analyze_D1():
    act_D1_raw = pd.read_excel('./data/N2 D1 vs. act1 D1 all differentials.xlsx')
    act_D1_raw = act_D1_raw.apply(add_log_2_fold_change, axis=1, args=("EDGE test: N2 D1 vs act1 D1, tagwise dispersions - Fold change",))



    column_mapper = {
        "Feature ID": "WormBaseID",
        "log2FoldChange": "log2FoldChange",
        "EDGE test: N2 D1 vs act1 D1, tagwise dispersions - P-value": "pvalue",
        "EDGE test: N2 D1 vs act1 D1, tagwise dispersions - FDR p-value correction": "padj",
    }

    act_D1_restructured = transform_upload(column_mapper, act_D1_raw)
    act_D1_restructured.to_csv("./data/restructured_act_D1.csv")

p1 = Process(target=analyze_D1)
p2 = Process(target=analyze_L4)
p1.start()
p2.start()