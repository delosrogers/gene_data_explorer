import models

def parse_query(query):
    print(query)
    tables = query.getlist('dataset')
    larryTables = query.getlist('larryDataset')
    initial_columns = query.getlist('column')
    additional_params = query['additional_params']
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
    return df, sql_statement