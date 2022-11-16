from flask import Flask, send_from_directory, request, url_for, send_file
from flask_restful import reqparse, Api
from flask_cors import CORS, cross_origin
from api.HelloApiHandler import HelloApiHandler
from textblob import TextBlob
from flask import Flask, jsonify, request, send_from_directory, send_file, redirect, url_for
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import requests
from bs4 import BeautifulSoup
import csv
import array as arr
import cleantext

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
api = Api(app)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get_image')
def get_image():
    filename = 'analyzed_histogram.png'
    return send_file(filename, mimetype='image/jpg')

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
    

@app.route("/url", methods=['GET','POST'])
@cross_origin()
def setURL():
    

    b = []
    c = [] 
    d = []     
    num = 0
    headers = {  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", }

    #for heat map and histogram axis labeling
    custom_bins = [-1.00,-0.8,-0.60,-0.40,-0.20,0.00,0.20,0.40,0.60,0.80,1.00]

    #the website magic
    app = Flask(__name__, static_folder='public')
            
    def printPage(item):
        url = request.json["url"]
        urls = url.split("/dp/")
        url = urls[0] + "/product-reviews/" + urls[1]
        urls = url.split("/ref=")
        urls[0] = urls[0] + "/ref=cm_cr_arp_d_paging_btm_next_"
        urls[1] = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  ('https://www.amazon.com/KOORUI-FreeSyncTM-Compatible-Ultra-Thin-24E4/dp/B09TTDRXNS/ref=cm_cr_arp_d_paging_btm_next_'+str(item)+'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(item))
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
            
    #use textblob to get subjectivity... 
    def getSubjectivity(text):
        return TextBlob(str(text)).sentiment.subjectivity
    #..and polarity
    def getPolarity(text):
        return TextBlob(str(text)).sentiment.polarity
    #the big function that does literall everything: "main"
    @app.route('/histograph')
    def analyzeCSV(hyperlink:str,kv:list=[]):

        #read the csv, then remove all purchases with no reviews
        reviews_data = pd.read_csv("tutorial.csv")
        reviews_data['entry'].replace('',np.nan,inplace=True)
        reviews_data.dropna(subset=['entry'],inplace=True)

        #add new sentimentality columns
        reviews_data['Subjectivity'] = reviews_data['entry'].apply(getSubjectivity)
        reviews_data['Polarity'] = reviews_data['entry'].apply(getPolarity)

        #sort reviews_data, then write to external file
        sorted_data = reviews_data.sort_values(by=['Polarity'])
        sorted_data.to_csv('analyzed_data.csv',index=False)
        
        createHistogram('analyzed_data.csv',kv)
        createHeatMap('analyzed_data.csv',kv)

    #enter a csv file and filter through key-value pairs to create a histogram
    #params: csv - string of file name
    #        kv - an (Nx2) array where kv[n][0] is the key to be filtered,
    #             and kv[n][1] is the value to be filtered for
    def createHistogram(csv_file:str,kv:list=[]):

        print(csv_file)
        analyzed_data = pd.read_csv(csv_file)
        #create a filtered dataframe
        
        print("TEST")
        
        for i in analyzed_data:
            print(str(analyzed_data[i]))
        
        # analyzed_data = filterDataFrame(analyzed_data,kv)
        
        # print("TEST")
        
        # for i in analyzed_data:
        #     print(str(analyzed_data[i]))
        
        colors = ["#d80a37","#a01e56","#e1c193","#ffd036","#ffe14d",
                "#ccff4e","#93d10e","#6bd40e","#2fc737","#2db33f"]
        
        #create historgram
        #custom_bins = [-1.00,-0.8,-0.60,-0.40,-0.20,0.00,0.20,0.40,0.60,0.80,1.00]
        
        print("TEST")
    
        
        n,m,patches = plt.hist(analyzed_data['Polarity'],bins = custom_bins)
        
        print("Anything: ")
        
        #color the gram
        for i in range(len(n)):
            c=colors[i]
            patches[i].set_fc(c)

        #format graph
        plt.title('Positivity of Reviews')
        plt.xlabel('Polarity')
        plt.xticks(custom_bins)
        plt.ylabel('Frequency')
        plt.tight_layout()

        out_file_name = 'analyzed_histogram'
        plt.savefig(out_file_name)
        #DEBUG: plt.show()
        
        #this might work idk
        #return send_file(out_file_name,mimetype='image/gif')

    #enter a csv file and filter through key-value pairs to create a heat map
    #params: csv - string of file name
    #        kv - an (Nx2) array where kv[n][0] is the key to be filtered,
    #             and kv[n][1] is the value to be filtered for    
    def createHeatMap(csv_file:str,kv:list=[]):
        
        analyzed_data = pd.read_csv(csv_file)
        
        #filter the dataframe
        # analyzed_data = filterDataFrame(analyzed_data,kv)
        
        #create the heat map
        map_data = {'Polarity':analyzed_data['Polarity'],
                    'Subjectivity':analyzed_data['Subjectivity']}
        map_data = pd.DataFrame(map_data)
        heatmap = heatmapNumPy(map_data)
        
        sns.heatmap(heatmap, cmap='RdPu')
        plt.title('Frequency of Sentimentalities')
        plt.ylabel('Polarity')
        plt.yticks(range(len(custom_bins)),labels=custom_bins,rotation=30)
        plt.rc('ytick',labelsize=7)
        plt.xlabel('Subjectivity')
        plt.xticks(range(len(custom_bins)),labels=custom_bins)
        plt.tight_layout()
        plt.savefig('analyzed_heatmap')
        #DEBUG:plt.show()
        
    #remove all elements of dataframe df which do not have any of the values matching the keys in kv
    def filterDataFrame(df:pd.DataFrame,kv:list=[]):
        #print('DEBUG: BEFORE FILTER:\n', analyzed_data.head())
        for key in kv:
            df = df.loc[df[key[0]] == key[1]]
        #print('DEBUG: AFTER FILTER:\n', analyzed_data.head())
        return df

    #find the frequency of occurrence of given Polarity and Subjectivity and convert to numpy array
    def heatmapNumPy(df:pd.DataFrame):
        interval = 0.20
        #custom_bins = [-1.00,-0.8,-0.60,-0.40,-0.20,0.00,0.20,0.40,0.60,0.80,1.00]
        result_heatmap = np.zeros((len(custom_bins),len(custom_bins)))
        for i in range(df['Polarity'].size):
            #print(df['Polarity'].array[i])
            pol = round(df['Polarity'].array[i]/interval) + int(len(custom_bins)/2)
            subj = round(df['Subjectivity'].array[i]/interval) + int(len(custom_bins)/2)
            result_heatmap[pol,subj]+=1
        
        return result_heatmap

    analyzeCSV('',[['location','india']])

if __name__ == '__main__':
    app.run()