from flask import Flask, send_from_directory, request, url_for, send_file, Response
from flask_restful import reqparse, Api
from flask_cors import CORS, cross_origin
from api.HelloApiHandler import HelloApiHandler
from textblob import TextBlob
from flask import Flask, jsonify, request, send_from_directory, send_file, redirect, url_for
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import requests
from bs4 import BeautifulSoup
import csv
import array as arr
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

@app.route('/get_image')
def get_image():
    filename = 'analyzed_histogram.svg'
    return send_file(filename, mimetype='image/svg+xml')

@app.route('/image/<svgFile>')
def serve_image(svgFile):
    return send_file(svgFile, mimetype='image/svg+xml')

@app.route('/filterupdate', methods=['GET','POST'])
def filterupdate():
    request.json["date"]
    request.json["location"]
    ancsv.analyzeCSV([[]])

@app.route("/api", methods=['POST'])
@cross_origin()
def bull():
    url = request.json["url"]
    urls = url.split("/dp/")
    url = urls[0] + "/product-reviews/" + urls[1]
    urls = url.split("/ref=")
    urls[0] = urls[0] + "/ref=cm_cr_arp_d_paging_btm_next_"
    urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
    print(urls[0] + str(1) + urls[1] + str(1))

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

    #the website magic
    app = Flask(__name__, static_folder='public')
            
    def printPage(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = urls[0] + "/product-reviews/" + urls[1]
        urls = url.split("/ref=")
        urls[0] = urls[0] + "/ref=cm_cr_arp_d_paging_btm_next_"
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

    # def printPageAu(item2):

    #     url2 =  ('https://www.amazon.com.' + 'au' + '/crocs-Unisex-Classic-Black-Women/product-reviews/B0014BYHJE/ref=cm_cr_arp_d_paging_btm_next_'+str(item2)+'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(item2))
    #     webpage2 = requests.get(url2, headers=headers)
    #     soup2 = BeautifulSoup(webpage2.content, "html.parser")
    #     reviews2 = soup2.find_all('div', {'data-hook': 'review'})
        
    #     for i in reviews2:
    #         b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text,no_emoji=True))
    #         splitter2 = i.find('span', {'data-hook' : 'review-date'}).text.split('in')
    #         c.append(cleantext.clean(splitter2[1].split('on')[0],no_emoji=True))
    #         d.append(splitter2[1].split('on')[1])
            
    # def printPageCA(item3):

    #     url3 =  ('https://www.amazon.'+'ca'+'/crocs-Unisex-Classic-Black-Women/product-reviews/B0014BYHJE/ref=cm_cr_arp_d_paging_btm_next_'+str(item3)+'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(item3))
    #     webpage3 = requests.get(url3, headers=headers)
    #     soup3 = BeautifulSoup(webpage3.content, "html.parser")
    #     reviews3 = soup3.find_all('div', {'data-hook': 'review'})
        
    #     for i in reviews3:
    #         b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text,no_emoji=True))
    #         splitter3 = i.find('span', {'data-hook' : 'review-date'}).text.split('in')
    #         c.append(cleantext.clean(splitter3[1].split('on')[0],no_emoji=True))
    #         d.append(splitter3[1].split('on')[1])
            
    # def printPageUK(item4):

    #     url4 =  ('https://www.amazon.'+'in'+'/crocs-Unisex-Classic-Black-Women/product-reviews/B0014BYHJE/ref=cm_cr_arp_d_paging_btm_next_'+str(item4)+'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(item4))
    #     webpage4 = requests.get(url4, headers=headers)
    #     soup4 = BeautifulSoup(webpage4.content, "html.parser")
    #     reviews4 = soup4.find_all('div', {'data-hook': 'review'})
        
    #     for i in reviews4:
    #         b.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text,no_emoji=True))
    #         splitter4 = i.find('span', {'data-hook' : 'review-date'}).text.split('in')
    #         c.append(cleantext.clean(splitter4[1].split('on')[0],no_emoji=True))
    #         d.append(splitter4[1].split('on')[1])

    for page in range(50):
        b.append(printPage(page+1))
        
    # for page2 in range(10):
    #     b.append(printPageAu(page2+1))

    # for page3 in range(50):
    #     b.append(printPageCA(page3+1))

    # for page4 in range(20):
    #     b.append(printPageUK(page4+1))
        
    with open('tutorial.csv', 'w', newline ='') as csvfile:
        fieldnames = ['number', 'entry', 'location', 'date']
        
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
            thewriter.writerow({'number':num, 'entry':b[num-1], 'location':count, 'date':d[num-1]  })
            
    ancsv.analyzeCSV([['date', ' December 1, 2022']])

    plt.close()

if __name__ == '__main__':
    app.run()