import gene_data_explorer.models as models
from flask import render_template, Markup
from flask import make_response
from gene_data_explorer.config import COLUMN_DICT, TABLE_DICT, GENE_TYPE_DICT
from clustergrammer2 import Network
import numpy as np
from gene_data_explorer.models import Authorized_user_emails, User
from gene_data_explorer import db
from werkzeug.datastructures import ImmutableMultiDict
import pandas as pd


# def parse_query(query: ImmutableMultiDict):
#     """Takes a query in the form of an immutable multidict and turns it into
#     a list of string tables and columns which are passed to the models join_data()
#     function where they are parsed into ORM objects and a dataframe is returned"""
#     print(query)
#     tables = query.getlist('dataset')
#     return_missing = query.get('return_missing')
#     additional_params = query.get('additional_params')
#     if not(additional_params):
#         additional_params = ""
#     if query.get("RNAi"):
#         columns = ["genes.WormBaseID", "genes.GeneName", "genes.sequence"]
#         if "Vidal_RNAi" in tables:
#             for i in "vidal_plate vidal_row vidal_col".split(" "):
#                 columns.append(TABLE_DICT['Vidal_RNAi'] + "." + COLUMN_DICT[i])
#         if "Ahringer_RNAi" in tables:
#             for i in "ahringer_plate ahringer_well".split(" "):
#                 columns.append(
#                     TABLE_DICT['Ahringer_RNAi'] + "." + COLUMN_DICT[i])

#     # This is a RNAseq data query not RNAi so process using the make_table_and_col_lists() fuction
#     else:
#         columns, tables = _make_table_and_col_lists(
#             query, tables, additional_params)
#     genes_str = query['genes']
#     genes = genes_str.split('\r\n')
#     gene_type = GENE_TYPE_DICT[query.get('gene_type')]
#     df, sql_statement = models.join_data(
#         columns, tables, genes, additional_params=additional_params, return_missing=return_missing, gene_type=gene_type)
#     """ if len(df)>1:
#         print('{type_} here'.format(type_=type(df.loc[0,df.columns[0]])))
#         df = df.sort_values(by = df.columns[0], axis = 0, ascending = True) """
#     return df, sql_statement


def parse_RNAseq_query(query: ImmutableMultiDict):
    """ builds the table and column lists based off the query and deseq tables that have been asked for
    by iterating through all the types of datasets and translating to the real column names """
    tables = query.getlist('dataset')
    return_missing = query.get('return_missing')
    additional_params = query.get('additional_params')
    larryTables = query.getlist('larryDataset')
    cco1_jmjd_tables = query.getlist('cco1_jmjd_Dataset')
    requested_columns = query.getlist('column')
    beccaTaylor_tables = query.getlist('Becca_taylor_dataset')
    if len(additional_params.split(";")) > 1:
        raise Exception("Not allowed to use semicolons")
    q_list = list(query.values())
    print(q_list)
    columns = ['genes.WormBaseID', 'genes.GeneName', 'genes.sequence']
    for i in tables:
        for j in requested_columns:
            columns.append(TABLE_DICT[i] + "." + COLUMN_DICT[j])
    # translates the checkbox data for Eps-8 into columns for the SQL join
    for i in larryTables:
        for j in requested_columns:
            if (COLUMN_DICT[j] == 'log2FoldChange'):
                columns.append(i + "." + COLUMN_DICT["larry_log2FoldChange"])
            elif (COLUMN_DICT[j] == 'pvalue'):
                columns.append(i + "." + COLUMN_DICT["Larry_PValue"])
            elif(COLUMN_DICT[j] == 'padj'):
                columns.append(i + "." + COLUMN_DICT["Larry_Padj"])
    tables += larryTables

    # Translates checkbox data for Becca Taylor's neuron specific RNAseq
    if len(beccaTaylor_tables) > 0:
        beccaTaylorTableName = "Rebecca_Taylor_neuronal_RNAseq_xbp-1"
        for i in requested_columns:
            if (COLUMN_DICT[i] == 'log2FoldChange'):
                columns.append(beccaTaylorTableName + "." +
                               COLUMN_DICT["log2FoldChange"])
            elif (COLUMN_DICT[i] == "padj"):
                columns.append(beccaTaylorTableName + "." + COLUMN_DICT["FDR"])
        tables.append(beccaTaylorTableName)
    # translates the checkbox data for cco1 and jmjd into columns for the SQL join
    cco1_translation_dict = {
        'log2FoldChange': 'Log2FC',
        'lfcSE': 'LfcSE',
        'padj': 'Padj',
        'pvalue': 'Pval',
        'cco1': 'Cco1',
        'sur5::jmjd1.2': 'Sur5',
        "rgef::jmjd1.2": 'Rgef',
        "jmjd:3.1::jmjd:3.1": 'Jmjd'
    }
    if cco1_jmjd_tables:
        for i in cco1_jmjd_tables:
            for j in requested_columns:
                if j in "log2FoldChange pvalue padj lfcSE".split(" "):
                    col = cco1_translation_dict[i] + cco1_translation_dict[j]
                    columns.append("cco1_jmjd_RNAseq." + col)
        tables.append("cco1_jmjd_RNAseq")

    tables = list(set(tables))
    print(tables)

    genes_str = query['genes']
    genes = genes_str.splitlines()
    # tell the database if you are using WB IDs, gene Names, or sequence names
    gene_type = GENE_TYPE_DICT[query.get('gene_type')]
    df, sql_statement = models.join_data(
        columns, tables, genes, return_missing=return_missing, gene_type=gene_type)
    """ if len(df)>1:
        print('{type_} here'.format(type_=type(df.loc[0,df.columns[0]])))
        df = df.sort_values(by = df.columns[0], axis = 0, ascending = True) """
    return df, sql_statement


def get_db_info() -> pd.DataFrame:
    """ retrieves a dataframe of all tables and columns in the database """
    res = models.get_db_info()
    return res

def parse_RNAi_query(query: ImmutableMultiDict) -> tuple:
    """ takes immutable multidict from post request for a RNAi
    request and processes it into a list of columns and tables 
    as strings and sends it to models.join_data and returns a dataframe
    """

    print(query)
    tables = query.getlist('dataset')
    return_missing = query.get('return_missing')
    additional_params = query.get('additional_params')
    if not(additional_params):
        additional_params = ""
    columns = ["genes.WormBaseID", "genes.GeneName", "genes.sequence"]

    if "Vidal_RNAi" in tables:
        for i in "vidal_plate vidal_row vidal_col".split(" "):
            columns.append(TABLE_DICT['Vidal_RNAi'] + "." + COLUMN_DICT[i])

    if "Ahringer_RNAi" in tables:
        for i in "ahringer_plate ahringer_well".split(" "):
            columns.append(
                TABLE_DICT['Ahringer_RNAi'] + "." + COLUMN_DICT[i])
    
    genes_str = query['genes']
    genes = genes_str.splitlines()
    # tell the database if you are using WB IDs, gene Names, or sequence names
    gene_type = GENE_TYPE_DICT[query.get('gene_type')]
    df, sql_statement = models.join_data(
        columns, tables, genes, return_missing=return_missing, gene_type=gene_type)
    """ if len(df)>1:
        print('{type_} here'.format(type_=type(df.loc[0,df.columns[0]])))
        df = df.sort_values(by = df.columns[0], axis = 0, ascending = True) """
    return df, sql_statement

def send_download(df: pd.DataFrame):
    resp = make_response(df.to_csv(sep="\t"))
    resp.headers["Content-Disposition"] = "attachment; filename=result.txt"
    resp.headers["Content-Type"] = "text/csv"
    return resp


def make_clustergrammer(df: pd.DataFrame):
    df.set_index('genes.GeneName', inplace=True)
    df.drop("genes.WormBaseID", inplace=True, axis=1)
    df.dropna(inplace=True)
    df = df[df.applymap(np.isreal).all(1)]
    net = Network()
    net.load_df(df)
    net.swap_nan_for_zero()
    net.cluster(dist_type='euclidean')
    viz = net.export_net_json()
    return render_template('clustergrammer.html', viz=viz)


def render_html_table(df: pd.DataFrame):
    return render_template(
        'table.html',
        column_names=df.columns.values,
        row_data=list(df.values.tolist()),
        link_column="genes.WormBaseID",
        zip=zip,
    )


def render_table_heatmap_or_download(df: pd.DataFrame):
    """ used to make and parse post requests from the forms used to query RNAseq and RNAi data """
    if request.method == 'POST':  # this block is only entered when the form is submitted
        query = request.form

        result, sql_statement = parse_query(query)
        result = result.apply(
            replace_empty_gene_name_with_wbid_or_sequence, axis=1)
        if not(query.get('sequence_names') == "True"):
            result = result.drop('genes.sequence', axis=1)
        if query['download_type'] == "tsv":
            resp = make_response(result.to_csv(sep="\t"))
            resp.headers["Content-Disposition"] = "attachment; filename=result.txt"
            resp.headers["Content-Type"] = "text/csv"
            return resp
        elif query['download_type'] == "clustergrammer":
            # make sure there are no missing index labels
            result.set_index('genes.GeneName', inplace=True)
            result.drop("genes.WormBaseID", inplace=True, axis=1)
            result.dropna(inplace=True)
            result = result[result.applymap(np.isreal).all(1)]
            net = Network()
            net.load_df(result)
            net.swap_nan_for_zero()
            net.cluster(dist_type='euclidean')
            viz = net.export_net_json()
            return render_template('clustergrammer.html', viz=viz)
        else:
            return render_template('table.html', column_names=result.columns.values, row_data=list(result.values.tolist()), link_column="genes.WormBaseID", zip=zip)

    return render_template(file)


def get_gene_info(gene):
    """ will return gene annotations when those are added to db """
    result = models.get_gene_info(gene)
    return render_template('table.html', column_names=result.columns.values, row_data=list(result.values.tolist()), link_column="", zip=zip)


# used for formating clustergrammer input
def replace_empty_gene_name_with_wbid_or_sequence(row):
    """ used to make sure there is always a gene name """
    if row['genes.GeneName'] == "" and row['genes.sequence'] != "":
        row["genes.GeneName"] = row["genes.sequence"]
    elif row['genes.sequence'] == "":
        row["genes.GeneName"] = row["genes.WormBaseID"]
    return row


class UserManagement:
    """ manages adding and removing/authorizing users """
    @staticmethod
    def authorize_email(email):
        Authorized_user_emails.add_email(email)
        User.authorize_by_email(email)
        print('authorizing{email} in UserManagement'.format(email=email))

    @staticmethod
    def deauthorize_email(email):
        Authorized_user_emails.remove_email(email)
        User.deauthorize_by_email(email)

    @staticmethod
    def is_email_authorized(email):
        print('authorized_email')
        authed_emails = db.session.query(Authorized_user_emails.email).all()
        authorized = [item for t in authed_emails for item in t]
        print(authorized, 'auth_emails')
        if email in authorized:
            authed = True
        else:
            authed = False
        print('authed', authed)
        return authed