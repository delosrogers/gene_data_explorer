import mysql.connector
from mysql.connector import Error
import pandas as pd
def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database='gene_data',
            port=6603,

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def make_table(data, name, connection):
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT gid FROM " + name + ";")
    all_gids = column_to_list(cursor.fetchall())
    missing = test_for_missing_wbids(data, connection, name)
    j=0
    for i in data.index:
        j += 1
        if (j % 100 == 0):
            print(str(i) + " " + name)
        try:
            cursor.execute("SELECT gid FROM genes WHERE WormBaseID = %(wbid)s;", {'wbid': i})
            res = cursor.fetchall()
            if (len(res) < 1):
                raise Exception("WBID " +i+ " is missing from the genes table")
            gid = list(res[0])
            row = list(data.loc[i])
            row = replace_nan_with_none(row)
            values = tuple(gid + row)
            #print(i)
            if gid[0] in all_gids:
                cursor.execute(
                    "UPDATE " + name + " SET \
                    gid = %s, \
                    baseMean = %s, \
                    log2FoldChange = %s, \
                    lfcSE = %s, \
                    stat = %s, \
                    pvalue = %s, \
                    padj = %s \
                    WHERE gid = " +str(gid[0]) + ";",
                    values)
                connection.commit()
            else:
                cursor.execute(
                    "INSERT INTO " + name  + "(gid, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj) \
                    Values (%s, %s, %s, %s, %s, %s, %s);", values
                    )
                connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
    cursor.close()
    return missing

def make_larry_table(data, name, connection):
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT gid FROM " + name + ";")
    all_gids = column_to_list(cursor.fetchall())
    missing = test_for_missing_wbids(data, connection, name)
    j = 0;
    for i in data.index:
        j += 1
        if (j % 100 == 0):
            print(str(i) + " " + name)
        try:
            cursor.execute("SELECT gid FROM genes WHERE WormBaseID = %(wbid)s;", {'wbid': i})
            gid_res = cursor.fetchall()
            if (len(gid_res) < 1):
                raise Exception("WBID " +i+ " is missing from the genes table")
            gid = list(gid_res[0])
            row = list(data.loc[i])
            row = replace_nan_with_none(row)
            row[0] = int(row[0])
            row[1] = int(row[1])
            values = tuple(gid + row)
            #print(i)
            if gid[0] in all_gids:
                cursor.execute(
                    "UPDATE " + name + " SET \
                    gid = %s, \
                    `Experiment - Range (original values)` = %s, \
                    `Experiment - IQR (original values)` = %s, \
                    `Experiment - Difference (original values)` = %s, \
                    `Experiment - Fold Change (original values)` = %s, \
                    `Experiment - Range (normalized values)` = %s, \
                    `Experiment - IQR (normalized values)` = %s, \
                    `Experiment - Difference (normalized values)` = %s, \
                    `Experiment - Fold Change (normalized values)` = %s, \
                    `Experiment - Range (transformed values)` = %s, \
                    `Experiment - IQR (transformed values)` = %s, \
                    `Experiment - Difference (transformed values)` = %s, \
                    `Experiment - Fold Change (transformed values)` = %s, \
                    `Annotations - Ensembl` = %s, \
                    `Combined names` = %s, \
                    `tagwise dispersions - Fold change` = %s, \
                    `tagwise dispersions - P-value` = %s, \
                    `tagwise dispersions - FDR p-value correction` = %s, \
                    `tagwise dispersions - Weighted difference` = %s, \
                    `tagwise dispersions - Bonferroni` = %s, \
                    `Annotations - GO molecular function` = %s, \
                    `Annotations - GO biological process` = %s, \
                    `Annotations - GO cellular component` = %s, \
                    `Annotations - Ensembl Description` = %s \
                    WHERE gid = " +str(gid[0]) + ";",
                    values)
                connection.commit()
            else:
                    cursor.execute(
                        "INSERT INTO " + name  + "(gid, \
                        `Experiment - Range (original values)`, \
                        `Experiment - IQR (original values)`, \
                        `Experiment - Difference (original values)`,\
                        `Experiment - Fold Change (original values)`,	\
                        `Experiment - Range (normalized values)`,	\
                        `Experiment - IQR (normalized values)`, \
                        `Experiment - Difference (normalized values)`, \
                        `Experiment - Fold Change (normalized values)`, \
                        `Experiment - Range (transformed values)`, \
                        `Experiment - IQR (transformed values)`, \
                        `Experiment - Difference (transformed values)`, \
                        `Experiment - Fold Change (Transformed values)`, \
                        `Annotations - Ensembl`, \
                        `Combined names`, \
                        `tagwise dispersions - Fold change`, \
                        `tagwise dispersions - P-value`, \
                        `tagwise dispersions - FDR p-value correction`, \
                        `tagwise dispersions - Weighted difference`, \
                        `tagwise dispersions - Bonferroni`, \
                        `Annotations - GO molecular function`, \
                        `Annotations - GO biological process`, \
                        `Annotations - GO cellular component`, \
                        `Annotations - Ensembl Description`) \
                        Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", values
                        )
                    connection.commit()
        except Error as e:
            print(f"The error '{e}' occured")
            print(i)
    cursor.close()
    return missing

def column_to_list(column):
    res = []
    for i in column:
        res.append(i[0])
    return res

def replace_nan_with_none(l : list) -> list:
    for i in range(len(l)):
        if (pd.isna(l[i]) or l[i] == "?" or l[i] == "-?" or l[i] == "nan"):
            l[i] = None
            #print("encountered a non integer or float")
    return l

def test_for_missing_wbids(data: pd.DataFrame, connection, name: str) -> set:
    cursor = connection.cursor()
    cursor.execute("SELECT WormBaseID FROM genes;")
    all_db_wbids = column_to_list(cursor.fetchall())
    missing_ids = []
    for i in data.index:
        if not(i in all_db_wbids):
            missing_ids.append(i)
            cursor.execute("INSERT INTO genes(WormBaseID, GeneName) Values (%s, %s)", (i, "this gene is questionable and was added because it appeared in " +name))
            connection.commit()
    if (len(missing_ids)>0):
        print("these id's are missing:" + str(missing_ids))
    return set(missing_ids)