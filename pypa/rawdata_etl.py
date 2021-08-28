"""
This module is to collect raw data from database
Authored: Phuong V. Nguyen
Dated: August 24th, 2021
"""
import cx_Oracle
import pandas as pd
import datetime
import dateutil
from dateutil.parser import parse
from dateutil.rrule import rrule, MONTHLY, WEEKLY, DAILY
import calendar
import timeit
import itertools
from phuong_omg_params import *
cx_Oracle.init_oracle_client(lib_dir=path_cx)

def connection(username, password):
    dns = cx_Oracle.makedsn(host='', port=, service_name='')
    conn = cx_Oracle.connect(username, password, dns)

    return conn

def fmcgdb_connection(username,password):
    """
    This function is to make connection to datasource. User must provide his/her user and password
    :return conn: the connection
    """
    dns = cx_Oracle.makedsn(host='', port=, service_name='')
    conn = cx_Oracle.connect(username, password, dns)
    return conn


def Data_query(query,conn):
    # print('I am querying data from dwh-db.techcombank.com.vn. Pls wait, Sir!\n...')
    sql_data = pd.read_sql(query, conn)
    print(sql_data)
    return sql_data



# if __name__=='__main__':

    # conn = connection(user, password)
    # start = timeit.default_timer()
    # for i, j in zip(begin_month, end_month):
    #     start = timeit.default_timer()
    #     print('I am querying data from {}'.format(i) +' to {} \n...'.format(j))
    #     atm_weekda = atm_weekday.format(i, j)
    #     # print(atm_weekda)
    #     dt = Data_query(atm_weekda, conn)
    #     print('data save to: '+ phuong_atm +'up_todate={}.csv'.format(j))
    #     dt.to_csv(phuong_atm+'up_todate={}.csv'.format(j),index=False)
    #     stop = timeit.default_timer()
    #     print('time: %.2f'%(stop-start))
    #
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
