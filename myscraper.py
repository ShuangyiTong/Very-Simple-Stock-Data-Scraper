import urllib.request as urlreq
import datetime
import pandas as pd
import time
import sys
import os

class myscraper:

    def __init__(self):
        self.date = datetime.date.today()

    def netease_stock_retriver(self, url_prefix='http://quotes.money.163.com/trade/lszjlx_',stock_code=600415,stop_page=999):
        current_page = 0
        while True:
            url = 'http://quotes.money.163.com/trade/lszjlx_' + str(stock_code) + ','+str(current_page)+'.html'
            print('Get data from ', url)
            while True:
                try:
                    session = urlreq.urlopen(url,timeout=3)
                    html_string = session.read()
                # Sometimes NetEase will reset connection, then we just sleep for 3 seconds.
                except urllib.error:
                    time.sleep(3)
                    continue
                print("    Page size is ", sys.getsizeof(html_string))
                if current_page==stop_page or sys.getsizeof(html_string) < 30000:
                    return
                path = os.path.join(os.path.join(os.getcwd(), str(stock_code)), str(self.date))
                if not os.path.exists(path):
                    os.makedirs(path)
                html_file_name = os.path.join(path, str(stock_code) + '_'+str(current_page)+'.html')
                html_file = open(html_file_name,'wb')
                html_file.write(html_string)
                html_file.close()
                table = pd.read_html(html_file_name)[3]
                csv_name = os.path.join(path, str(stock_code) + '_'+str(current_page)+'.csv')
                table.to_csv(csv_name,encoding='utf-8')
                current_page+=1
                break