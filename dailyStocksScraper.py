#! python3
# dailyStocksScraper.py - Logs the data of any stock details after stock symbols entered 
# into the command line

import requests, sys, os, bs4, csv
from pathlib import Path
from datetime import datetime, date

if len(sys.argv) > 1:
    symbols = [i.upper() for i in sys.argv[1:]]
else:
    print("You didn't enter any symbols. Try running the program again.")
    sys.exit()

print("\nEnter the address where you want to save the stock details (Note: Add quotations around the address):")

i = 0
while True:
    path = input()
    address = Path(r"{}".format(path.replace("\"", "").replace("'", "")))
    if os.path.isdir(address):
        break
    elif i == 3:
        print("Unfortunately you have reached the acceptable number of attempts. \nGoodbye.")
        sys.exit()
    else:
        print(f"That address is incorrect. Try again. {address}")
        i += 1

stocksFile = open(address / f"{datetime.today().strftime('%d_%m_%Y')}_stocks.txt", "w+")
stocksFile.write(f"\t\tDate Accessed - {datetime.today().strftime('%d_%m_%Y')}")
stocksFile.write("\n\n")

start_date = datetime(2023, 4, 29)

for symbol in symbols:
    stocksFile.write(f"{symbol} - \n")
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136"}
    res = requests.get(f"https://uk.finance.yahoo.com/quote/{symbol}/history?p=AAPL", headers=header)
    try:
        sort = bs4.BeautifulSoup(res.text, 'html.parser')
        csvLink = sort.select('a[class = "Fl(end) Mt(3px) Cur(p)"]')[0].get("href")
        csvRequest = requests.get(csvLink, headers=header)
        csvFile = open(f"{symbol}.csv", "wb")
        for chunk in csvRequest.iter_content(100000):
            csvFile.write(chunk)
        csvFile.close()
    except res.raise_for_status():
        print("*** HTTPError: Website request has failed. ***")

stocksFile.close()
print("\nDone.")