import pandas as pd
import gene_data_explorer.models as models
import io
import json


def upload_data(request):
    form_query = request.form
    req_file = request.file.get('upload')
    buff = io.StringIO(req_file.read())
    filename = req_file.filename
    if not(allowed_file(filename)):
        return "Bad upload"

    df = pd.read_csv(buff)

    if form_query.get('gene_type') == "GeneName":
        df = add_wormbase_ID(df, form_query.get("gene_name_column"))
    column_mapper = Json.loads(form_query.get("column_mapper"))
    transformed_df = transform_upload(column_mapper, df)
    name = query_form.get('name')
    result_df = models.upload_RNAseq_df(transformed_df, name) 


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['csv'])
    return filename.split(".")[1] in ALLOWED_EXTENSIONS


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


def add_wormbase_ID(df: pd.DataFrame, gene_name_column: str) -> pd.DataFrame:
    gene_name_to_WBID = models.get_gene_table()
    gene_name_to_WBID = gene_name_to_WBID.set_index('GeneName')
    df = df.apply(_add_wbid_in_apply, axis=1, args=(gene_name_to_WBID, gene_name_column))
    return df


def _add_wbid_in_apply(
        row: pd.Series,
        gene_name_to_WBID: pd.DataFrame,
        gene_name_column) -> pd.Series:
    row['WormBaseID'] = gene_name_to_WBID.loc[row[gene_name_column], "WormBaseID"]
    return row
