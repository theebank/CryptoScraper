from flask.json import jsonify
import re
import time

# from bs4 import BeautifulSoup
from flask import Flask
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import psycopg2


app = Flask(__name__)

# Testing Data
with open("testdata.json") as json_file:
    testdata = json.load(json_file)


def upload_cryptodata(jsondata):
    try:
        cryptodataconn = psycopg2.connect(
            database="postgres",
            user="pythonpostgres",
            password="12345",
            host="localhost",
            port="5432",
        )
        insertquery_cryptodata = """insert into cryptodata (coinname, price, daterecorded) values (%s, %s, %s)"""

        cursor = cryptodataconn.cursor()

        cursor.execute("select version()")

        data = cursor.fetchone()
        print("Connection established to: ", data)

        f = "%Y-%m-%d %H:%M:%S"
        currtime = time.strftime(f, time.localtime())

        for entry in jsondata["data"]:
            values_to_insert = (
                entry["name"],
                entry["quote"]["USD"]["price"],
                currtime,
            )

            cursor.execute(insertquery_cryptodata, values_to_insert)

        cryptodataconn.commit()
        count = cursor.rowcount()
        print(count, "Record(s) inserted")
    except (Exception, psycopg2.Error) as error:
        print("failed to insert", error)


def get_page_data_webscrape():
    webscrapeURL = "https://coinmarketcap.com/"
    # sc-482c3d57-3 iTyfmj cmc-table - prev table id
    # sc-dba2d818-3 iWUxTT cmc-table - prev table id
    # sc-\w{8}-3 i\w{5} cmc-table - regex

    # ret type array of objects
    page = requests.get(webscrapeURL)

    soup = BeautifulSoup(page.content, "html.parser")
    # need to find a way to get this dynamically updating

    maindiv = soup.find(
        "table", class_=re.compile(r"sc-\w{8}-3 i\w{5} cmc-table")
    )  # needs to be tested on another day if works
    tabledata = maindiv.tbody.find_all("tr")

    topten = []
    for j in range(0, 10):
        i = tabledata[j]
        row = i.find_all("td")
        name = row[2].div.a.div.p.text
        price = row[3].div.a.span.text
        objtoadd = {"name": name, "price": float(price[1:].replace(",", ""))}
        topten.append(objtoadd)
    for j in range(10, 100):
        i = tabledata[j]
        row = i.find_all("td")
        name = row[2].a.findChildren()[1].text
        price = row[3].span.text
        objtoadd = {"name": name, "price": float(price[1:].replace(",", ""))}
        topten.append(objtoadd)

    print(topten)
    return topten


def get_page_data_api():
    cmcURL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {"start": "1", "limit": "100", "convert": "CAD"}

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "f3fbffb3-7a65-4dec-bd03-12cd8b62295f",
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(cmcURL, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def main():
    print(get_page_data_webscrape())


@app.route("/getdata")
def getdata():
    # test3

    # data = get_page_data_api()
    # newdata = downloadandmodify(data)
    # return(newdata)

    # upload_cryptodata(testdata)
    return jsonify(testdata)


if __name__ == "__main__":
    app.run()
