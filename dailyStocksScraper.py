#! python3
# dailyStocksScraper.py - Logs the data of any stock details after stock symbols entered 
# into the command line

import requests, sys
from pathlib import Path

print("Enter the symbol(s) for the stocks:")
print()

if len(sys.argv) > 1:
    symbols = [i.upper() for i in sys.argv[1:]]
else:
    print("You didn't enter anything. Try running the program again.")
    sys.exit()

print("Enter the address where you want to save the stock details:")
print()
i = 0
while True:
    address = Path(input().replace("\"", "").replace("\'", ""))
    if address.is_file():
        break
    elif i == 3:
        print("Unfortunately you have reached the acceptable number of attempts. \nGoodbye.")
        sys.exit()
    else:
        print("That address is incorrect. Try again.")
        i += 1

for symbol in symbols:
    res = requests.get(f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=1651067896&period2=1682603896&interval=1d&events=history&includeAdjustedClose=true")
    res.raise_for_status()
    stockFile = open(f"{symbol}.csv", "wb")
    for chunk in res.iter_content(100000):
        stockFile.write(chunk)
    