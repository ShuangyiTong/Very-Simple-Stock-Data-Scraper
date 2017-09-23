import myscraper
from itertools import islice

ns = myscraper.myscraper()

with open('Shanghai_Stock_Code_List', 'r') as f:
    stock_code_list = f.readlines()

for i, stock_code in islice(enumerate(stock_code_list),0,947):
    print(str(i/9.47).strip() + '% completed')
    ns.netease_stock_retriver(stock_code=(int(stock_code.strip())))
