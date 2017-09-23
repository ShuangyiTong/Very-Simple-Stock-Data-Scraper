# Very-Simple-Stock-Data-Scraper
Low performance webpage stock data scraper

Current this scraper retrieve webpage from NetEase Finance, mainly focus on Shanghai stock market.

run the following command to get all 947 stock data
```
python3 run_scraper.py
```
then run the following command to push these data to a sqlite3 database
```
python3 push_data.py
```

In `myscraper.py` and `dbmgr.py`, there are more options for finer control over data scraping and pushing.

Originally, this scraper was connected with LAMSTAR program with old Huaji Script which tried to analyze those data. Obviously, using LAMSTAR to predict stock market was a mistake. (Studies show it might be useful in high-frequency trading)

Now Huaji Script can complete more complex task, so maybe I will improve LAMSTAR model (like multilayer) and try again.