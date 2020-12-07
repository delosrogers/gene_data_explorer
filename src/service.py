import models

def parse_query(query):
    print(query)
    q_list = list(query.values())
    print(q_list)
    tables = []
    columns = ['genes.WormBaseID', 'genes.GeneName']
    for i in range(len(q_list)-1):
        tmp_table = q_list[i].split(".")
        print(tmp_table)
        tables.append(tmp_table[0])
        columns.append(q_list[i])
    tables = list(set(tables))
    print(tables)
    genes_str = query['genes']
    genes = genes_str.split('\r\n')
    db = models.geneModel() 
    df = db.join_data(columns, tables, genes)
    return df