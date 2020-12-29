import importlib
import gene_data_explorer.models as models
import gene_data_explorer.service as service
from werkzeug.datastructures import MultiDict
import numpy as np
from pathlib import Path
import pandas as pd
import math

def test_parse_query_RNAi():
    #tests wether by passing columns and genes to the parse query function you can do a library lookup
    query_dict = MultiDict([("dataset", "Vidal_RNAi"),("genes", "WBGene00000885"),("return_missing","False"),("additional_params", ""),('gene_type','WBID'),("RNAi", "RNAi_screen")])
    df, stmnt = service.parse_query(query_dict)
    real_result = np.array(pd.DataFrame([("WBGene00000885", "cyn-9", 10002, "E", 5),("WBGene00000885", "cyn-9", 11053, "B", 2)]))
    print(np.array(df))
    print(real_result)
    assert np.array_equal(np.array(df),real_result)

def test_parse_query_RNAi_vidal_ahringer():
    #tests wether by passing columns and genes to the parse query function you can do a library lookup
    real_result_df = pd.read_csv(Path('./gene_data_explorer/test_data/RNAi_lookup_test_data.csv'))
    genes = list(real_result_df['Gene ID'])
    gene_str = "\r\n".join(genes)
    query_dict = MultiDict([("dataset", "Vidal_RNAi"), ("dataset", "Ahringer_RNAi"),("genes", gene_str),("return_missing","True"),("additional_params", ""),("RNAi", "RNAi_screen"),('gene_type','WBID')])
    df, stmnt = service.parse_query(query_dict)
    for i in real_result_df.index:
        for j in real_result_df.columns:
            if real_result_df.loc[i,j] is None or pd.isna(real_result_df.loc[i, j]) or  real_result_df.loc[i,j] == "nan":
                print(real_result_df.loc[i,j])
                print(type(real_result_df.loc[i,j]))
                real_result_df.loc[i, j] = "None"
    for i in df.index:
        
        for j in df.columns:
            print(df.loc[i,j])
            print(type(df.loc[i,j]))
            if pd.isna(df.loc[i, j]) or df.loc[i,j] == "nan" or df.loc[i,j] is None:
                df.loc[i, j] = "None"
    real_result = np.array(real_result_df)
    print(np.array(df))
    print(real_result)
    print(np.array(df) == real_result)
    assert (np.array(df) == real_result).all()