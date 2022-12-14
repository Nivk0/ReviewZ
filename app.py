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


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
api = Api(app)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

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
        ancsv.createHistogram('analyzed_data.csv',[['month', month]])
        ancsv.createHeatMap('analyzed_data.csv',[['month', month]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    elif (month == ""):
        ancsv.createHistogram('analyzed_data.csv',[['location', location]])
        ancsv.createHeatMap('analyzed_data.csv',[['location', location]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        ancsv.createHistogram('analyzed_data.csv',[['location', location], ['month', month]])
        ancsv.createHeatMap('analyzed_data.csv',[['location', location], ['month', month]])
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
    if (exists("analyzed_histogram.svg")):
            os.remove("analyzed_histogram.svg")
    if (exists("analyzed_heatmap.svg")):
        os.remove("analyzed_heatmap.svg")
    return Response("Success", status=200, mimetype='application/text')
    

@app.route("/url", methods=['GET','POST'])
@cross_origin()
def setURL():
    
    b = []
    c = [] 
    d = []     
    num = 0
    headers = {  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", }

    # If the url is invalid, returns message

    url = request.json["url"]
    if (url.rfind("/dp/") == -1):
        if(url==""):
            response = make_response(jsonify({"message": "Please enter a url."}), 200,)
        else:
            response = make_response(jsonify({"message": "The link is invalid. Please try another link."}), 200, )
        response.headers["Content-Type"] = "application/json"
        return response
    
    #
    #   Web Scraping Begins Here
    #
            
    def printPage(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = "https://amazon.com/product-reviews/" + urls[1][0:10]
        urls[0] = url + "/ref=cm_cr_arp_d_paging_btm_next_"
        urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urls[0] +str(item)+ urls[1] + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            c.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            d.append(splitter[1].split('on')[-1])

    def printPageAu(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = "https://amazon.com.au/product-reviews/" + urls[1][0:10]
        urls[0] = url + "/ref=cm_cr_arp_d_paging_btm_next_"
        urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urls[0] +str(item)+ urls[1] + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            c.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            d.append(splitter[1].split('on')[-1])
            
    def printPageCA(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = "https://amazon.ca/product-reviews/" + urls[1][0:10]
        urls[0] = url + "/ref=cm_cr_arp_d_paging_btm_next_"
        urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urls[0] +str(item)+ urls[1] + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            c.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            d.append(splitter[1].split('on')[-1])
            
    def printPageIN(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = "https://amazon.in/product-reviews/" + urls[1][0:10]
        urls[0] = url + "/ref=cm_cr_arp_d_paging_btm_next_"
        urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urls[0] +str(item)+ urls[1] + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            c.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            d.append(splitter[1].split('on')[-1])

    def printpageUK(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = "https://amazon.co.uk/product-reviews/" + urls[1][0:10]
        urls[0] = url + "/ref=cm_cr_arp_d_paging_btm_next_"
        urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urls[0] +str(item)+ urls[1] + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            c.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            d.append(splitter[1].split('on')[-1])

    for page in range(50):
        b.append(printPage(page+1))
        
    for page2 in range(2):
        b.append(printPageAu(page2+1))

    for page3 in range(50):
        b.append(printPageCA(page3+1))

    for page4 in range(2):
        b.append(printPageIN(page4+1))
    
    for page5 in range(10):
        b.append(printpageUK(page5+1))
    
    # Creates the tutorial csv
    
    with open('tutorial.csv', 'w', newline ='') as csvfile:
        fieldnames = ['number', 'entry', 'location', 'month']
        
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        
        #DEBUG
        # print('DEBUG:',len(c))
        # print('DEBUG:',len(b))
        # print('DEBUG',len(d))
        for count in c:
            num+=1
            
            #DEBUG
            # print('DEBUG:',num)
            # print('DEBUG',b[num-1])
            c[num-1]
            month = d[num-1].split(" ")[1]   #splits the date and returns the month
            thewriter.writerow({'number':num, 'entry':b[num-1], 'location':count, 'month':month  })
    
    # Creates ONLY the anaylzed csv
    ancsv.analyzeCSV([[]])

    plt.close()

    response = make_response(jsonify({"message": "Success"}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run()