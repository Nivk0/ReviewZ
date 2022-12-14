from textblob import TextBlob
import matplotlib as mpl
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import exists
plt.style.use('fivethirtyeight')

mpl.use("svg")

#for heat map and histogram axis labeling
custom_bins = [-1.00,-0.8,-0.60,-0.40,-0.20,0.00,0.20,0.40,0.60,0.80,1.00]

#use textblob to get subjectivity... 
def getSubjectivity(text):
    return TextBlob(str(text)).sentiment.subjectivity
#..and polarity
def getPolarity(text):
    return TextBlob(str(text)).sentiment.polarity
#the big function that does literall everything: "main"

def analyzeCSV(kv:list=[]):
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
    
    analyzed_data = filterDataFrame(analyzed_data,kv)
    
    colors = ["#d80a37","#a01e56","#e1c193","#ffd036","#ffe14d",
            "#ccff4e","#93d10e","#6bd40e","#2fc737","#2db33f"]
    
    #create historgram
    #custom_bins = [-1.00,-0.8,-0.60,-0.40,-0.20,0.00,0.20,0.40,0.60,0.80,1.00]

    n,m,patches = plt.hist(analyzed_data['Polarity'],bins = custom_bins)
    
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
    analyzed_data = filterDataFrame(analyzed_data,kv)
    
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
    # print('DEBUG: BEFORE FILTER:\n', df.head())
    for key in kv:
        if(len(key) != 0):
            df = df.loc[df[key[0]] == key[1]]
    # print('DEBUG: AFTER FILTER:\n', df.head())
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

def plotClose():
    plt.close()