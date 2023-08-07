import requests
from bs4 import BeautifulSoup


def get_total_debt(ticker):
    return get_esg_tile_value(f"https://www.macroaxis.com/financial-statements/{ticker}/Total-Debt")


def get_shareholders_equity(ticker):
    return get_esg_tile_value(f"https://www.macroaxis.com/financial-statements/{ticker}/Shareholders-Equity-USD")


def get_esg_tile_value(url):
    micro_axis = requests.get(url).text
    soup = BeautifulSoup(micro_axis, "lxml")
    debt_text = soup.find("div", class_="esgTile p-l-10 p-r-10").text
    arr = debt_text.split(" ")
    amt = float(arr[0])
    ident = arr[1]

    if ident == "Billion":
        amt *= 1000000000
    elif ident == "Million":
        amt *= 1000000

    return amt
