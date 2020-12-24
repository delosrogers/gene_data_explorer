import models
from flask import render_template
from flask import make_response

def parse_query(query):
    print(query)
    tables = query.getlist('dataset')
    return_missing = query.get('return_missing')
    if query.get("RNAi"):
        columns = []
        if "Vidal_RNAi" in tables:
            columns += "Vidal_RNAi.CeRNAi_Plate ceRNAi_Row ceRNAi_Col".split(" ")
        if "Ahringer_RNAi" in tables:
            columns += "Ahringer_RNAi.Plate Ahringer_RNAi.Well".split(" ")
        additional_params=""
    else:
        columns, tables = _make_table_and_col_lists(query)
    genes_str = query['genes']
    genes = genes_str.split('\r\n')
    db = models.geneModel() 
    df, sql_statement = db.join_data(columns, tables, genes, additional_params=additional_params, return_missing=return_missing)
    db.cursor.close()
    db.conn.close()
    df.sort_values(by=df.columns[0], inplace=True)
    return df, sql_statement

def _make_table_and_col_lists(query):
    larryTables = query.getlist('larryDataset')
    initial_columns = query.getlist('column')
    additional_params = query['additional_params']
    if len(additional_params.split(";"))>1:
        raise Exception("Not allowed to use semicolons")
    q_list = list(query.values())
    print(q_list)
    columns = ['genes.WormBaseID', 'genes.GeneName']
    for i in tables:
        for j in initial_columns:
            columns.append(i + "." + j)
    for i in larryTables:
        for j in initial_columns:
            if (j == 'log2FoldChange'):
                columns.append(i + "." + j)
            elif (j == 'pvalue'):
                columns.append(i + "." + "TagwiseDispersionsPValue")
            elif(j == 'padj'):
                columns.append(i + "." + "TagwiseDispersionsFDRPValueCorrection")
    tables += larryTables
    tables = list(set(tables))
    print(tables)
    return colums, tables

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
            return '''{}<br> the SQL statement used was:<br>{}'''.format(result.to_html(), sql_statement)

    return render_template("{}".format(file))