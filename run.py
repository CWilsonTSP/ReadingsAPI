import json
import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    url = 'https://bible.usccb.org/daily-bible-reading'
    date = request.args.get('date')
    print(date)
    if date != None:
        url = 'https://bible.usccb.org/bible/readings/' + date + '.cfm'
        
    print(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get title
    titles = soup.select('div[class="innerblock"] > div[class="content-header"]')

    # get body
    readings = soup.select('div[class="innerblock"] > div[class="content-body"]')
    print(len(readings))

    # get verses
    verses = soup.select('div[class="innerblock"] > div[class="content-header"] > div[class="address"]')

    # get lectionary
    lectionary = soup.select('div[class="innerblock"] > p')

    # get title
    title = soup.select('div[class="innerblock"] > h2')
    if (len(readings)) == 4:
        rv = {
            "lectionary": lectionary[0].text,
            "title": title[0].text,
            "readings" : [
                {
                    "verse": verses[0].text,
                    "text": readings[0].text
                },
                {
                    "verse": verses[1].text,
                    "text": readings[1].text
                },
                {
                    "verse": verses[2].text,
                    "text": readings[2].text
                },
                {
                    "verse": verses[3].text,
                    "text": readings[3].text
                }
                ]
        }
    elif (len(readings) == 5):
        rv = {
            "lectionary": lectionary[0].text,
            "title": title[0].text,
            "readings" : [
                {
                    "verse": verses[0].text,
                    "text": readings[0].text
                },
                {
                    "verse": verses[1].text,
                    "text": readings[1].text
                },
                {
                    "verse": verses[2].text,
                    "text": readings[2].text
                },
                {
                    "verse": verses[3].text,
                    "text": readings[3].text
                },
                {
                    "verse": verses[4].text,
                    "text": readings[4].text
                }
                ]
        }
    else:
        return "Something went wrong", 400

    return jsonify(rv)



if __name__ == '__main__':
    app.run(debug=True)



