# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pymysql
import pymssql
from pandas.util.testing import assert_frame_equal
import datetime


def __diff_pd(df1, df2):
    """Identify differences between two pandas DataFrames"""
    assert (df1.columns == df2.columns).all(), "DataFrame column names are different"
    if df1.equals(df2):
        return None
    else:
        # need to account for np.nan != np.nan returning True
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        changed.index.names = ['id', 'col']
        difference_locations = np.where(diff_mask)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        return pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)


def mysql_table_compare(source_server, source_user, source_password, source_db, target_server, target_user,
                        target_password, target_db, table_charset, sql_script, quick_assert, output_result):
    source_connection = pymysql.connect(host=source_server, port=3306, user=source_user, passwd=source_password,
                                        charset=table_charset, db=source_db)

    target_connection = pymysql.connect(host=target_server, port=3306, user=target_user, passwd=target_password,
                                        charset=table_charset, db=target_db)
    chunk_size = 1000
    offset = 0
    df_slice_prod = []
    df_slice_dev = []
    df_slice_changed = []

    while True:
        sql_str = sql_script + " limit %d offset %d " % (chunk_size, offset)

        # In SQL Server 2012, we can use sql statement like this:
        # SELECT * FROM MyTable ORDER BY ID OFFSET 50 ROWS FETCH NEXT 25 ROWS ONLY;

        # In SQL Server 2005+, we can use SQL statement like this:
        # SELECT col1, col2
        # FROM(
        #       SELECT col1, col2,
        #              ROW_NUMBER() OVER(ORDER BY ID) AS RowNum
        #       FROM MyTable
        #      ) AS A
        # WHERE A.RowNum BETWEEN @ startRow AND @ endRow

        df_source = pd.read_sql(sql_str, con=source_connection)
        df_target = pd.read_sql(sql_str, con=target_connection)

        if quick_assert:
            try:
                assert_frame_equal(df_source, df_target)
            except AssertionError:
                source_connection.close()
                target_connection.close()
                return False
        else:
            df_changed = __diff_pd(df_source, df_target)
            df_slice_changed.append(df_changed)

        df_slice_prod.append(df_source)
        df_slice_dev.append(df_target)
        offset += chunk_size
        if len(df_slice_prod[-1]) < chunk_size:  # or len(df_slice_prod) == 2 # 先只跑2轮
            break

    source_connection.close()
    target_connection.close()

    if quick_assert:
        return True
    else:
        df_diff_result = pd.concat(df_slice_changed)
        df_diff_result.to_csv(output_result, sep='\t')
        return len(df_diff_result.index) == 0

    print "Compare Finished."


def test_compare_two_mysql_table():
    print datetime.datetime.now()

    # result1 = mysql_table_compare('geapidb61', 'AgentUser', 'wow!2010', 'GEAPI',
    #                              'geapidbdev81', 'GeDataAgent', '1234567#', 'GEAPI',
    #                              'utf8', "SELECT * FROM MSSDumpMangement order by OperationId", True,
    #                              "D:\\compare_result.csv")

    result = mysql_table_compare('geapidbdev81', 'GeDataAgent', '1234567#', 'GEAPI',
                                 'geapidbdev81', 'GeDataAgent', '1234567#', 'GEAPI',
                                 'utf8',
                                 "SELECT * FROM MSSDumpMangement where DataCategoryId=10104 and OperationId='0P000148AN' order by OperationId ",
                                 True,
                                 "D:\\compare_result.csv")
    if result:
        print "The tables are same."
    else:
        print "The tables are difference."

    print datetime.datetime.now()


def mssql_table_compare(source_server, source_user, source_password, source_db, target_server, target_user,
                        target_password, target_db, table_charset, sql_script, quick_assert, output_result):
    source_connection = pymssql.connect(server=source_server, port=1433, user=source_user, password=source_password,
                                        charset=table_charset, database=source_db)

    target_connection = pymssql.connect(server=target_server, port=1433, user=target_user, password=target_password,
                                        charset=table_charset, database=target_db)
    chunk_size = 1000
    offset = 0
    df_slice_prod = []
    df_slice_dev = []
    df_slice_changed = []

    while True:
        sql_str = sql_script + " OFFSET %d ROWS FETCH NEXT %d ROWS ONLY;" % (offset, chunk_size)

        # In SQL Server 2012, we can use sql statement like this:
        # SELECT * FROM MyTable ORDER BY ID OFFSET 50 ROWS FETCH NEXT 25 ROWS ONLY;

        # In SQL Server 2005+, we can use SQL statement like this:
        # SELECT col1, col2
        # FROM(
        #       SELECT col1, col2,
        #              ROW_NUMBER() OVER(ORDER BY ID) AS RowNum
        #       FROM MyTable
        #      ) AS A
        # WHERE A.RowNum BETWEEN @ startRow AND @ endRow

        df_source = pd.read_sql(sql_str, con=source_connection)
        df_target = pd.read_sql(sql_str, con=target_connection)

        if quick_assert:
            try:
                assert_frame_equal(df_source, df_target)
            except AssertionError:
                source_connection.close()
                target_connection.close()
                return False
        else:
            df_changed = __diff_pd(df_source, df_target)
            df_slice_changed.append(df_changed)

        df_slice_prod.append(df_source)
        df_slice_dev.append(df_target)
        offset += chunk_size
        if len(df_slice_prod[-1]) < chunk_size:  # or len(df_slice_prod) == 2 # 先只跑2轮
            break

    source_connection.close()
    target_connection.close()

    if quick_assert:
        return True
    else:
        df_diff_result = pd.concat(df_slice_changed)
        df_diff_result.to_csv(output_result, sep='\t')

    print "Compare Finished."


def main():
    print ""


if __name__ == '__main__':
    main()
