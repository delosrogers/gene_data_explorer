import models
def parse_query(query):
    print(query)
    q_list = list(query.values())
    print("something went wrong")
    tables = ['genes']
    columns = ['genes.WormBaseID', 'genes.GeneName']
    for i in range(len(q_list)-1):
        tables.append(q_list[i])
        columns.append(q_list[i] + '.log2FoldChange')
    genes_str = query['genes']
    genes = genes_str.split('\r\n')
    db = models.geneModel() 
    df = db.join_data(columns, tables, genes)
    return df.to_html()