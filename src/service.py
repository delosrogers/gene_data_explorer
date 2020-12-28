import models
from flask import render_template, Markup
from flask import make_response
from config import COLUMN_DICT, TABLE_DICT, GENE_TYPE_DICT

def parse_query(query):
    print(query)
    tables = query.getlist('dataset')
    return_missing = query.get('return_missing')
    additional_params = query.get('additional_params')
    if not(additional_params):
        additional_params=""
    if query.get("RNAi"):
        columns = ["genes.WormBaseID", "genes.GeneName"]
        if "Vidal_RNAi" in tables:
            for i in "vidal_plate vidal_row vidal_col".split(" "):
                columns.append(TABLE_DICT['Vidal_RNAi'] + "." + COLUMN_DICT[i])
        if "Ahringer_RNAi" in tables:
            for i in "ahringer_plate ahringer_well".split(" "):
                columns.append(TABLE_DICT['Ahringer_RNAi'] + "." + COLUMN_DICT[i])
    else:
        columns, tables = _make_table_and_col_lists(query, tables, additional_params)
    genes_str = query['genes']
    genes = genes_str.split('\r\n')
    db = models.geneModel()
    gene_type = GENE_TYPE_DICT[query.get('gene_type')] 
    df, sql_statement = db.join_data(columns, tables, genes, additional_params=additional_params, return_missing=return_missing, gene_type=gene_type)
    db.cursor.close()
    db.conn.close()
    df.sort_values(by=df.columns[0], inplace=True)
    return df, sql_statement

def _make_table_and_col_lists(query, tables, additional_params):
    larryTables = query.getlist('larryDataset')
    cco1_jmjd_tables = query.getlist('cco1_jmjd_Dataset')
    requested_columns = query.getlist('column')
    if len(additional_params.split(";"))>1:
        raise Exception("Not allowed to use semicolons")
    q_list = list(query.values())
    print(q_list)
    columns = ['genes.WormBaseID', 'genes.GeneName']
    for i in tables:
        for j in requested_columns:
            columns.append(TABLE_DICT[i] + "." + COLUMN_DICT[j])
    #translates the checkbox data for Eps-8 into columns for the SQL join
    for i in larryTables:
        for j in requested_columns:
            if (COLUMN_DICT[j] == 'log2FoldChange'):
                columns.append(i + "." + COLUMN_DICT["larry_log2FoldChange"])
            elif (COLUMN_DICT[j] == 'pvalue'):
                columns.append(i + "." + COLUMN_DICT["Larry_PValue"])
            elif(COLUMN_DICT[j] == 'padj'):
                columns.append(i + "." + COLUMN_DICT["Larry_Padj"])
    tables += larryTables
    #translates the checkbox data for cco1 and jmjd into columns for the SQL join
    cco1_translation_dict = {
        'log2FoldChange': 'Log2FC', 
        'lfcSE': 'LfcSE',
        'padj': 'Padj',
        'pvalue': 'Pval',
        'cco1': 'Cco1',
        'sur5::jmjd1.2':'Sur5',
        "rgef::jmjd1.2":'Rgef',
        "jmjd:3.1::jmjd:3.1":'Jmjd'
        }
    if cco1_jmjd_tables:
        for i in cco1_jmjd_tables:
            for j in requested_columns:
                if j in "log2FoldChange pvalue padg lfcSE".split(" "):
                    col = cco1_translation_dict[i] + cco1_translation_dict[j]
                    columns.append("cco1_jmjd_RNAseq." + col)
        tables.append("cco1_jmjd_RNAseq")
    
    tables = list(set(tables))
    print(tables)
    return columns, tables

def get_db_info():
    db = models.geneModel()
    res = db.get_info()
    db.cursor.close()
    db.conn.close()
    return res

def db_form(request, file):
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query = request.form

        result, sql_statement = parse_query(query)
        resp = make_response(result.to_csv(sep="\t"))
        resp.headers["Content-Disposition"] = "attachment; filename=result.txt"
        resp.headers["Content-Type"] = "text/csv"
        if query['download_type']=="tsv":
            return resp
        else:
            return render_template('table.html',table = Markup(result.to_html()), sql_statement = sql_statement)

    return render_template("{}".format(file))