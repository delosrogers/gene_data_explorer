import importlib
importlib.import_module('..models', 'src')
importlib.import_module('..service', 'src')
from werkzeug.datastructures import MultiDict
import numpy as np
from pathlib import Path
import pandas as pd

def test_parse_query_RNAi():
    #tests wether by passing columns and genes to the parse query function you can do a library lookup
    query_dict = MultiDict([("dataset", "Vidal_RNAi"), ("column", "ceRNAi_Plate"), ("column", "ceRNAi_Row"), ("column", "ceRNAi_Col"),("genes", "WBGene00000885"),("return_missing","False"),("additional_params", "")])
    df, stmnt = service.parse_query(query_dict)
    real_result = np.array(pd.DataFrame([("WBGene00000885", "cyn-9", 10002, "E", 5),("WBGene00000885", "cyn-9", 11053, "B", 2)]))
    print(np.array(df))
    print(real_result)
    assert np.array_equal(np.array(df),real_result)

def test_parse_query_RNAi_vidal_ahringer()
    #tests wether by passing columns and genes to the parse query function you can do a library lookup
    real_result_df = pd.read_csv(Path('./test_data/RNAi_lookup_test_data.csv'))
    genes = list(real_result['Gene ID'])
    gene_str = "\r\n".join(genes)
    query_dict = MultiDict([("dataset", "Vidal_RNAi"), ("dataset", "Ahringer_RNAi"),("genes", gene_str),("return_missing","True"),("additional_params", "")])
    df, stmnt = service.parse_query(query_dict)
    real_result = np.array(real_result_df))
    print(np.array(df))
    print(real_result)
    assert np.array_equal(np.array(df),real_result)