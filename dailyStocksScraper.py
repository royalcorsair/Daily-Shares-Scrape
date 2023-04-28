#! python3
# dailyStocksScraper.py - Logs the data of any stock details after stock symbols entered 
# into the command line

import requests, sys, os
from pathlib import Path
from datetime import datetime
import yfinance as yf

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
stocksFile.write(f"\t\tDate Accessed - {datetime}")
stocksFile.write("\n\n")

start_date = datetime(2023, 4, 26)

for symbol in symbols:
    stocksFile.write(f"{symbol} - \n")
    data = yf.download(symbol, start=start_date)
    stocksFile.write(f"{data}\n\n")

stocksFile.close()
print("\nDone.")