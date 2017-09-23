import dbmgr as sm
import datetime
from itertools import islice

today = '/' + str(datetime.date.today()) + '/'

with open('Shanghai_Stock_Code_List', 'r') as f:
    stock_code_list = f.readlines()

for i, stock_code in islice(enumerate(stock_code_list),0,947):
    print(str(i/9.47).strip() + '% completed')
    db = sm.sqlite3_stock_dbmgr('ShanghaiStock.db',str(stock_code).strip())
    file_prefix = './' + str(stock_code).strip() + today + str(stock_code).strip() + '_'
    print(file_prefix)
    db.push_csv(csvfile_prefix=file_prefix, end_iterator=21, end_row=51, enable_print=False)
    db.commit_and_close()