import sqlite3
import csv
from datetime import datetime, timedelta
from itertools import islice

class sqlite3_stock_dbmgr:

    def __init__(self, dbname, tablename):
        self.tablename = tablename
        self.conn = sqlite3.connect(dbname)
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS '%s' (date NUMERIC PRIMARY KEY UNIQUE, close_price REAL, close_price_change REAL, 
                                                        turnover ratio REAL, inflow_fund REAL, outflow_fund REAL, 
                                                        net_inflow_fund REAL, main_inflow_fund REAL, main_outflow_fund REAL, 
                                                        net_main_inflow_fund REAL)""" % tablename)
    
    def push_csv(self, csvfile_prefix='./600415/2017-03-30/600415_', start_iterator=0, end_iterator=1, 
                 start_row=1, end_row=2, start_col=1, end_col=11, enable_print=False):
        cur = self.conn.cursor()
        for i in range(end_iterator)[start_iterator:]:
            try:
                with open(csvfile_prefix + str(i) + '.csv', newline='', encoding='utf-8') as csvfile:
                    spamreader = csv.reader(csvfile)
                    for j, row in islice(enumerate(spamreader),start_row,end_row):
                        values = '\',\''.join(row[start_col:end_col])
                        if enable_print:
                            print("'%s'" % values)
                        cur.execute("INSERT INTO '%s' VALUES ('%s')" % (self.tablename, values))
            except:
                return

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()

    def post_processing_after_fetchone(self,fetched_data):
        if fetched_data is not None:
            return str(fetched_data[0]).strip('%') + ",\n"
        else:
            return ''
    
    def post_processing_after_fetchall(self,fetched_data,start_col,end_col):
        if fetched_data is not None:
            return_string = ""
            for i in range(end_col)[start_col:]:
                return_string+=str(fetched_data[i]).strip('%') + ",\n"
            return return_string
        else:
            return ''

    def prepare_csv_data_coloumn_first(self, start_date, end_date, start_col=1, end_col=2, filename='test.csv'):
        data_file = open(filename, 'w')
        cur = self.conn.execute("SELECT * FROM '%s'" % self.tablename)
        raw_list_of_coloumns = cur.description
        list_of_coloumns = []
        for i in range(end_col)[start_col:]:
            list_of_coloumns.append(raw_list_of_coloumns[i][0])
        for coloumns in list_of_coloumns:
            current_date = start_date
            while current_date != end_date:
                cur.execute("SELECT %s FROM  '%s' WHERE date='%s'" % (coloumns, self.tablename, current_date))
                data_file.write(self.post_processing_after_fetchone(cur.fetchone()))
                date_obj = datetime.strptime(current_date, "%Y-%m-%d")
                date_obj = date_obj + timedelta(days=1)
                current_date = datetime.strftime(date_obj, "%Y-%m-%d")
        data_file.close()

    def prepare_csv_data_row_first(self, start_date, end_date, start_col=1, end_col=2, filename='test.csv'):
        data_file = open(filename, 'w')
        cur = self.conn.cursor()
        current_date = start_date
        while current_date != end_date:
            cur.execute("SELECT * FROM  '%s' WHERE date='%s'" % (self.tablename, current_date))
            data_file.write(self.post_processing_after_fetchall(cur.fetchone(),start_col,end_col))
            date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            date_obj = date_obj + timedelta(days=1)
            current_date = datetime.strftime(date_obj, "%Y-%m-%d")
        data_file.close()