import models

def parse_query(query):
    print(query)
    tables = query.getlist('dataset')
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
    genes_str = query['genes']
    genes = genes_str.split('\r\n')
    db = models.geneModel() 
    df, sql_statement = db.join_data(columns, tables, genes, additional_params=additional_params)
    db.cursor.close()
    db.conn.close()
    return df, sql_statement

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
    return db.get_info()
