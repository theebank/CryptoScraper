import random
from flask.json import jsonify
import requests
import re
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)


@app.route("/getdata")
def hello_world():
    data = get_page_data()

    
    return jsonify({"datalist":data})




URL = "https://coinmarketcap.com/"
#sc-482c3d57-3 iTyfmj cmc-table
#sc-dba2d818-3 iWUxTT cmc-table
#regex sc-\w{8}-3 i\w{5} cmc-table

def get_page_data():
    #ret type array of objects
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    # need to find a way to get this dynamically updating

    maindiv = soup.find("table", class_=re.compile(r'sc-\w{8}-3 i\w{5} cmc-table'))#needs to be tested on another day if works
    tabledata = maindiv.tbody.find_all("tr")

    topten = []
    for j in range(0, 10):
        i = tabledata[j]
        row = i.find_all("td")
        name = row[2].div.a.div.p.text
        price = row[3].div.a.span.text
        objtoadd = {
            "name": name,
            "price": float(price[1:].replace(",", ""))
        }
        topten.append(objtoadd)
    for j in range(10, 100):
        i = tabledata[j]
        row = i.find_all("td")
        name = row[2].a.findChildren()[1].text
        price = row[3].span.text
        objtoadd = {
            "name": name,
            "price": float(price[1:].replace(",", ""))
        }
        topten.append(objtoadd)

    print(topten)
    return topten


def main():
    print(get_page_data())


if __name__ == "__main__":
    app.run()
