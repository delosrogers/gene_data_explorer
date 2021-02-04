import importlib
import gene_data_explorer.models as models
import gene_data_explorer.service as service
import gene_data_explorer.uploadData as uploadData
from werkzeug.datastructures import MultiDict
import numpy as np
from pathlib import Path
import pandas as pd
import math


def test_parse_query_RNAi():
    # tests wether by passing columns and genes to the parse query function you can do a library lookup
    query_dict = MultiDict(
        [("dataset", "Vidal_RNAi"), ("genes", "WBGene00000885"),
        ("return_missing", "False"), ("additional_params", ""),
        ('gene_type', 'WBID'), ("RNAi", "RNAi_screen")])
    df, stmnt = service.parse_RNAi_query(query_dict)
    df = df.drop("genes.sequence", axis=1)
    real_result = np.array(pd.DataFrame(
        [("WBGene00000885", "cyn-9", 10002, "E", 5), ("WBGene00000885", "cyn-9", 11053, "B", 2)]))
    print(np.array(df))
    print(real_result)
    assert np.array_equal(np.array(df), real_result)


def test_parse_query_RNAi_vidal_ahringer():
    # tests wether by passing columns and genes to the parse query function you can do a library lookup
    real_result_df = pd.read_csv(
        Path('./gene_data_explorer/test_data/RNAi_lookup_test_data.csv'))
    genes = list(real_result_df['Gene ID'])
    gene_str = "\r\n".join(genes)
    query_dict = MultiDict([("dataset", "Vidal_RNAi"), ("dataset", "Ahringer_RNAi"), ("genes", gene_str), (
        "return_missing", "True"), ("additional_params", ""), ("RNAi", "RNAi_screen"), ('gene_type', 'WBID')])
    df, stmnt = service.parse_RNAi_query(query_dict)
    df = df.drop("genes.sequence", axis=1)
    for i in real_result_df.index:
        for j in real_result_df.columns:
            if real_result_df.loc[i, j] is None or pd.isna(real_result_df.loc[i, j]) or real_result_df.loc[i, j] == "nan":
                real_result_df.loc[i, j] = "None"
    for i in df.index:

        for j in df.columns:
            print(df.loc[i, j])
            print(type(df.loc[i, j]))
            if pd.isna(df.loc[i, j]) or df.loc[i, j] == "nan" or df.loc[i, j] is None:
                df.loc[i, j] = "None"
    real_result = np.array(real_result_df)
    print(np.array(df))
    print(real_result)
    print(np.array(df) == real_result)
    assert (np.array(df) == real_result).all()


def test_parse_query_RNAseq_data():
    real_result_df = pd.read_csv(
        Path('./gene_data_explorer/test_data/RNAseq_data_test_outer_join.csv'))
    genes = list(real_result_df['WBID'])
    gene_str = "\r\n".join(genes)
    query_dict = MultiDict([
        ("dataset", "tph1p_v_N2"),
        ("dataset", "dat1p_v_N2"),
        ("dataset", "dat1p_tph1p_v_N2"),
        ("dataset", "rab3p_v_N2"),
        ("larryDataset", "eps8_RNAi"),
        ("cco1_jmjd_Dataset", "sur5::jmjd1.2"),
        ("cco1_jmjd_Dataset", "rgef::jmjd1.2"),
        ("column", "log2FoldChange"),
        ("column", "pvalue"),
        ("column", "padj"),
        ("genes", gene_str),
        ("additional_params", ""),
        ("gene_type", "WBID"),
        ("return_missing", "True")
    ])
    print(query_dict)
    df, stmt = service.parse_RNAseq_query(query_dict)
    df = df.drop("genes.sequence", axis=1)
    real_result = np.array(real_result_df)

    for i in real_result_df.index:
        for j in real_result_df.columns:
            if real_result_df.loc[i, j] is None or pd.isna(real_result_df.loc[i, j]) or real_result_df.loc[i, j] == "nan":
                real_result_df.loc[i, j] = -1
    for i in df.index:

        for j in df.columns:
            if pd.isna(df.loc[i, j]) or df.loc[i, j] == "nan" or df.loc[i, j] is None:
                df.loc[i, j] = -1

    arr = np.array(df[df.columns[2:20]]).astype(float)
    real_result = np.array(
        real_result_df[real_result_df.columns[2:20]]).astype(float)
    sentinal = True
    print(arr)
    print(real_result)
    for i in range(len(arr)):
        for j in range(len(arr[i])):

            sentinal = sentinal and math.isclose(
                float(arr[i, j]), float(real_result[i, j]), rel_tol=1E-06)
            print(math.isclose(float(arr[i, j]), float(
                real_result[i, j]), rel_tol=1E-06))

    assert sentinal


def test_transformData_for_upload():
    test_data = pd.DataFrame(
        [["SomeGene", 1, .1, .05, "blashsdf"]],
        columns=["WormBaseID", "coollog2FoldChange", "padj", "myPvalue", "another col"])
    real_result = pd.DataFrame(
        [["SomeGene", None, 1, None, None, .05, .1]],
        columns=["WormBaseID","baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj"]
    )
    columnMapper = {
        "WormBaseID": "WormBaseID",
        "coollog2FoldChange": "log2FoldChange",
        "padj": "padj",
        "myPvalue": "pvalue",
    }
    test_result = uploadData.transform_upload(columnMapper, test_data)
    assert test_result.equals(real_result)

def test_add_wormbase_ID():
    test_data = pd.DataFrame(
        [["hsp-4", 5]],
        columns=["GeneName", "log2FoldChange"]
    )
    real_result = pd.DataFrame(
        [["hsp-4", 5, "WBGene00002008"]],
        columns=["GeneName", "log2FoldChange", "WormBaseID"]
    )
    test_result = uploadData.add_wormbase_ID(test_data, "GeneName")
    assert test_result.equals(real_result)
