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
    titles = soup.select('div[class="innerblock"] > div[class="content-header"] > h3[class="name"]')

    # get body
    readings = soup.select('div[class="innerblock"] > div[class="content-body"]')
    print(len(readings))

    # get verses
    verses = soup.select('div[class="innerblock"] > div[class="content-header"] > div[class="address"]')

    # get lectionary
    lectionary = soup.select('div[class="innerblock"] > p')

    # get title
    title = soup.select('div[class="innerblock"] > h2')

    rv = {
            "lectionary": lectionary[0].text,
            "title": title[0].text.replace('\n', '')
        }

    reading_list = []
    for i in range(0, len(readings)):
        if i == 1:
            reading_list.append({
                        "title": titles[i].text.strip().replace('\n',''),
                        "verse": verses[i].text.strip().replace('\n', ''),
                        "text": readings[i].text.strip()
                    })
        else:
            reading_list.append({
                        "title": titles[i].text.strip().replace('\n',''),
                        "verse": verses[i].text.strip().replace('\n', ''),
                        "text": readings[i].text.strip().replace('\n', '')
                    })

    rv["readings"] = reading_list

    # if (len(readings)) == 4:
    #     rv = {
    #         "lectionary": lectionary[0].text,
    #         "title": title[0].text.replace('\n', ''),
    #         "readings" : [
    #             {
    #                 "title": titles[0].text.replace('\n',''),
    #                 "verse": verses[0].text.replace('\n', ''),
    #                 "text": readings[0].text.strip().replace('\n',' ').replace(u"\u00A0"," ").replace('  ',' ')
    #             },
    #             {
    #                 "verse": verses[1].text.replace('\n', ''),
    #                 "text": readings[1].text.strip()
    #             },
    #             {
    #                 "verse": verses[2].text.replace('\n', ''),
    #                 "text": readings[2].text.strip()
    #             },
    #             {
    #                 "verse": verses[3].text.replace('\n', ''),
    #                 "text": readings[3].text.strip().replace('\n',' ').replace(u"\u00A0"," ").replace('  ',' ')
    #             }
    #             ]
    #     }
    # elif (len(readings) == 5):
    #     rv = {
    #         "lectionary": lectionary[0].text,
    #         "title": title[0].text.replace('\n', ''),
    #         "readings" : [
    #             {
    #                 "verse": verses[0].text.replace('\n', ''),
    #                 "text": readings[0].text.strip().replace('\n',' ').replace(u"\u00A0"," ").replace('  ',' ')
    #             },
    #             {
    #                 "verse": verses[1].text.replace('\n', ''),
    #                 "text": readings[1].text.strip()
    #             },
    #             {
    #                 "verse": verses[2].text.replace('\n', ''),
    #                 "text": readings[2].text.strip().replace('\n',' ').replace(u"\u00A0"," ").replace('  ',' ')
    #             },
    #             {
    #                 "verse": verses[3].text.replace('\n', ''),
    #                 "text": readings[3].text.strip()
    #             },
    #             {
    #                 "verse": verses[4].text.replace('\n', ''),
    #                 "text": readings[4].text.strip().replace('\n',' ').replace(u"\u00A0"," ").replace('  ',' ')
    #             }
    #             ]
    #     }
    # else:
    #     return "Something went wrong", 400

    return jsonify(rv)



if __name__ == '__main__':
    app.run(debug=True)



