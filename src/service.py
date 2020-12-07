import models

def parse_query(query):
    print(query)
    tables = query.getlist('dataset')
    initial_columns = query.getlist('column')
    q_list = list(query.values())
    print(q_list)
    columns = ['genes.WormBaseID', 'genes.GeneName']
    for i in tables:
        for j in initial_columns:
            columns.append(i + "." + j)
    tables = list(set(tables))
    print(tables)
    genes_str = query['genes']
    genes = genes_str.split('\r\n')
    db = models.geneModel() 
    df = db.join_data(columns, tables, genes)
    return df