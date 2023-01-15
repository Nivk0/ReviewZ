import asyncio
from itertools import cycle
import re
import aiohttp
from flask import Flask, send_from_directory, request, send_file, Response, jsonify, make_response
from flask_restful import Api
from flask_cors import CORS, cross_origin
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import requests
from bs4 import BeautifulSoup
import csv
import cleantext
import os
from os.path import exists
import anaylzeCSV as ancsv
import appProxy as apPxy
import pandas as pd


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
api = Api(app)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/location-filter', methods=['GET'])
@cross_origin()
def location_filter():
    reviews_data = pd.read_csv("analyzed_data.csv")
    try:
        locations = reviews_data['Location'].drop_duplicates().sort_values().tolist()
        response = make_response(jsonify({'message': "Success", "locations": locations}), 200,)
    except Exception as err:
        print(f"Error occured in location-filter: {err}")
        response = make_response(jsonify({'message': "Failed to find locations"}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/image/<svgFile>') 
def serve_image(svgFile):
    return send_file(svgFile, mimetype='image/svg+xml')

@app.route('/filterupdate', methods=['GET','POST'])
def filterupdate():
    if (not exists("analyzed_data.csv")):
        response = make_response(jsonify({'message': "Image is being created. Please be patient."}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    if (exists("analyzed_histogram.svg")):
        os.remove("analyzed_histogram.svg")
    if (exists("analyzed_heatmap.svg")):
        os.remove("analyzed_heatmap.svg")
    try:
        month = request.json["month"]
    except:
        month = "";
    try:
        location = request.json["location"]
    except:
        location = ""
    if (location == "" and month == ""):
        ancsv.createHistogram('analyzed_data.csv',[[]])
        ancsv.createHeatMap('analyzed_data.csv',[[]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    elif (location == ""):
        ancsv.createHistogram('analyzed_data.csv',[['Month', month]])
        ancsv.createHeatMap('analyzed_data.csv',[['Month', month]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    elif (month == ""):
        ancsv.createHistogram('analyzed_data.csv',[['Location', location]])
        ancsv.createHeatMap('analyzed_data.csv',[['Location', location]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        ancsv.createHistogram('analyzed_data.csv',[['Location', location], ['Month', month]])
        ancsv.createHeatMap('analyzed_data.csv',[['Location', location], ['Month', month]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response

@app.route("/remove", methods=['GET'])
@cross_origin()
def remove():
    if (exists("tutorial.csv")):
        os.remove("tutorial.csv")
    if (exists("analyzed_data.csv")):
        os.remove("analyzed_data.csv")
    if (exists("proxies.csv")):
        os.remove("proxies.csv")
    if (exists("analyzed_histogram.svg")):
        os.remove("analyzed_histogram.svg")
    if (exists("analyzed_heatmap.svg")):
        os.remove("analyzed_heatmap.svg")
    return Response("Success", status=200, mimetype='application/text')

@app.route("/url", methods=['GET','POST'])
@cross_origin()
def setURL():
    # If the url is invalid, returns message
    URL = request.json["url"]
    
    # Declaration
    global urlBeginning, urlEnd, headers

    headers = [{ "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate", 
                "Referer": URL, },
               { "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate", 
                "Referer": URL, },
               { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate", 
                "Referer": URL, },
               { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate", 
                "Referer": URL, },
               { "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; Google Pixel Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 Mobile Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate", 
                "Referer": URL, }]

    if (URL.rfind("/dp/") == -1):
        if(URL==""):
            response = make_response(jsonify({"message": "Please enter a url."}), 200,)
        else:
            response = make_response(jsonify({"message": "The link is invalid. Please try another link."}), 200, )
    else:
            # Gives the Amazon ID
        amazonID = URL.split("/dp/")[1][0:10]
            # Gives the country domain of the amazon site
        amazonDomain = URL[0 : URL.find("/", 10)]
            # These will be used to scrape the data
        urlBeginning = amazonDomain + "/-/en/product-reviews/" + amazonID + "/ref=cm_cr_arp_d_paging_btm_next_"
        urlEnd = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        response = make_response(jsonify({"message": "Preparing to mine data from the sites."}), 200, )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/number-of-reviews", methods=['GET'])
@cross_origin()
def numberOfReviews():
    url =  (urlBeginning +str(1)+ urlEnd + str(1))
    print(url)
    
    webpage = requests.get(url, headers=headers[1])
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    if apPxy.isBlocked(soup):
        incrementor = 0
        while(apPxy.isBlocked(soup) and incrementor < len(headers)):
            print("BLOCKED")
            try:
                webpage = requests.get(url, headers=headers[incrementor], timeout=1)
                soup = BeautifulSoup(webpage.content, "html.parser")
                incrementor = incrementor + 1
            except:
                print("Connection error")
                incrementor = incrementor + 1
    
    try:
        commaNum = soup.find(string=re.compile("total ratings, ")).text.split("ratings, ")[1].split(" ")[0].split(",")
        global totalReviews 
        totalReviews = int(0)

        for index in range(len(commaNum)):
            totalReviews += int(commaNum[index]) * pow(1000, len(commaNum) - index - 1)
        
        response = make_response(jsonify({"message": totalReviews}), 200,)
    except:
        response = make_response(jsonify({"message": "Please try again."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/get-proxies", methods=['GET'])
@cross_origin()
def getProxies():
    response = make_response(jsonify({"message": "Proxies have been collected.", "proxies": apPxy.getProxies((urlBeginning +str(1)+ urlEnd + str(1)), totalReviews)}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response
        
#
#   Web Scraping Begins Here
#

@app.route("/scraper", methods=['GET', 'POST'])
@cross_origin()
def scrape_all():
    pageStart = int(request.json["page-start"])
    pageInterval = int(request.json["page-interval"])
    proxies = request.json["proxies"]
        
    async def printPage(session, pageNumber : int, cycle_headers : cycle, cycle_proxies : cycle):
        url = (urlBeginning + str(pageNumber) + urlEnd + str(pageNumber))
        
        try:
            response = await session.get(url, headers=next(cycle_headers), proxy=next(cycle_proxies), ssl=False, timeout=30)
            # response = await session.request(method="GET", url=url, proxy=nextP, ssl = False, timeout=10)
            webpage = await response.text()
            soup = BeautifulSoup(webpage, "html.parser")
            
            if not(apPxy.isBlocked(soup)):
                print("SUCCESS ", pageNumber)
                setCommentData(soup)
        except Exception as err:
            pass
            # DEBUG
            # print("Connection Error")
            # print(f"An error has occured: {err}")   
    
    def setCommentData(soup):
        reviewBodies = soup.find_all('span', {'data-hook' : 'review-body'})
        reviewDates =  soup.find_all('span', {'data-hook' : 'review-date'})
        
        for index in range(len(reviewBodies)):
            try:
                comment = cleantext.clean(reviewBodies[index].text, no_emoji=True)
            except:
                comment = "Not available"
            try:
                locationAndDate = reviewDates[index].text.split('in ') [1].split('on ') 
                location = cleantext.clean(locationAndDate[0], no_emoji=True)
                months = locationAndDate[1].split(" ")
                if (len(months[0]) > 2):
                    month = (months[0])
                else:
                    month = (months[1])
            except:
                location = "Other"
                month = "Not available"
            try:
                ancsv.anaCSV({'Review':comment, 'Location':location, 'Month':month })
            except Exception as err:
                print(f"Error writing comments: {err}")
        
    async def run():
        if (pageStart == 1):
            with open('analyzed_data.csv', 'w', newline ='') as csvfile:
                fieldnames = ['Polarity', 'Subjectivity', 'Review', 'Location', 'Month']
                thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                thewriter.writeheader()
        cycle_proxies = cycle(proxies)
        cycle_headers = cycle(headers)
        connector = aiohttp.TCPConnector(limit_per_host=50)
        async with aiohttp.ClientSession(connector = connector) as session:
            await asyncio.gather(*[printPage(session, pageNumber + pageStart, cycle_headers, cycle_proxies) for pageNumber in range(pageInterval)])
                
    print(f"start {pageStart} end {pageInterval}")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())

    response = make_response(jsonify({"message": "We have finished collecting all the reviews."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(threaded=True)