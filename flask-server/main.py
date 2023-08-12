import random
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    data = get_page_data()
    ret = ""
    for i in data:
        ret = ret + "[" + i[0] + "," + str(i[1]) + "]"
    return ret


URL = "https://coinmarketcap.com/"


def get_page_data():
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    maindiv = soup.find("table", class_="sc-482c3d57-3 iTyfmj cmc-table")
    # need to find a way to get this dynamically updating
    tabledata = maindiv.tbody.find_all("tr")

    topten = []
    for j in range(0, 10):
        i = tabledata[j]
        row = i.find_all("td")
        name = row[2].div.a.div.p.text
        price = row[3].div.a.span.text
        topten.append([name, float(price[1:].replace(",", ""))])
    for j in range(10, 100):
        i = tabledata[j]
        row = i.find_all("td")
        name = row[2].a.findChildren()[1].text
        price = row[3].span.text
        topten.append([name, float(price[1:].replace(",", ""))])

    print(topten)
    topten.sort(key=lambda x: x[1], reverse=True)

    print(topten)

    return topten


def main():
    print(get_page_data())


if __name__ == "__main__":
    main()
