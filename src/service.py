import models
from flask import render_template, Markup
from flask import make_response
from config import COLUMN_DICT, TABLE_DICT

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
    df, sql_statement = db.join_data(columns, tables, genes, additional_params=additional_params, return_missing=return_missing)
    db.cursor.close()
    db.conn.close()
    df.sort_values(by=df.columns[0], inplace=True)
    return df, sql_statement

def _make_table_and_col_lists(query, tables, additional_params):
    larryTables = query.getlist('larryDataset')
    initial_columns = query.getlist('column')
    if len(additional_params.split(";"))>1:
        raise Exception("Not allowed to use semicolons")
    q_list = list(query.values())
    print(q_list)
    columns = ['genes.WormBaseID', 'genes.GeneName']
    for i in tables:
        for j in initial_columns:
            columns.append(TABLE_DICT[i] + "." + COLUMN_DICT[j])
    for i in larryTables:
        for j in initial_columns:
            if (COLUMN_DICT[j] == 'log2FoldChange'):
                columns.append(i + "." + COLUMN_DICT["larry_log2FoldChange"])
            elif (COLUMN_DICT[j] == 'pvalue'):
                columns.append(i + "." + COLUMN_DICT["Larry_PValue"])
            elif(COLUMN_DICT[j] == 'padj'):
                columns.append(i + "." + COLUMN_DICT["Larry_Padj"])
    tables += larryTables
    tables = list(set(tables))
    print(tables)
    return columns, tables

# def parse_custom_query(form):
#     q_list = form['query'].split(" ")
#     query = form['query']
#     genes = form['genes']
#     if len(genes)>0:
#         if ("WHERE" in q_list):
#             if (q_list[len(q_list)-1] != "AND"):
#                 query += "AND"
#     begin = 1
#     end = q_list.index("FROM")
#     columns = q_list[begin:end]
#     db = models.geneModel()
#     df = db.make_query(query, columns, genes=genes)
#     sql_statement = db.cursor.statment
#     db.cursor.close()
#     db.conn.close()
#     return df, sql_statement

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