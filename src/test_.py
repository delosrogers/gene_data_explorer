import models
import service
from werkzeug.datastructures import MultiDict
import numpy as np
import pandas as pd

def test_parse_query_RNAi():
    #tests wether by passing columns and genes to the parse query function you can do a library lookup
    query_dict = MultiDict([("dataset", "Vidal_RNAi"), ("column", "ceRNAi_Plate"), ("column", "ceRNAi_Row"), ("column", "ceRNAi_Col"),("genes", "WBGene00000885"),("return_missing","False"),("additional_params", "")])
    df, stmnt = service.parse_query(query_dict)
    real_result = np.array(pd.DataFrame([("WBGene00000885", "cyn-9", 10002, "E", 5),("WBGene00000885", "cyn-9", 11053, "B", 2)]))
    print(np.array(df))
    print(real_result)
    assert np.array_equal(np.array(df),real_result)