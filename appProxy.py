import asyncio
import csv
import re
import aiohttp
from bs4 import BeautifulSoup
import requests
import headers as hdrs

headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate", }

def isBlocked(soup):
    blockedMessage = soup.find("p", {"class": "a-last"})
    return not(blockedMessage is None)

def getProxies(url, totalReviews):
    async def writeCSV():
        with open('proxies.csv', 'w', newline ='') as csvfile:
            fieldnames = ['proxies']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            
            proxies = await scrapeProxies(url, totalReviews)
            for proxy in proxies:
                thewriter.writerow({'proxies': proxy})
                
    def readCSV():
        proxies = []
        with open('proxies.csv', newline ='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row["proxies"])
                proxies.append(row["proxies"])
        return proxies
    
    asyncio.new_event_loop().run_until_complete(writeCSV())
    return readCSV()

async def scrapeProxies(url, totalReviews):
        proxy_url = "https://free-proxy-list.net/"
        response = requests.get(proxy_url, headers=headers)
        webpage = BeautifulSoup(response.content, "html.parser")
        rawProxies = webpage.find("tbody")
        structuredProxies = rawProxies("tr", limit=100)
        # random.shuffle(structuredProxies)
        # randomProxies = list()
        # for index in range(12):
        #     randomProxies.append(structuredProxies[index])
        proxies = list()
        
        async with aiohttp.ClientSession(headers=hdrs.headers[0]) as session:
            await asyncio.gather(*[testProxy(session, url, proxies, proxy, totalReviews) for proxy in structuredProxies])
        
        # for randomProxy in randomProxies:
        #     ip = randomProxy.find("td")
        #     proxies.append(ip.text + ":" + ip.next_sibling.text)
        return proxies
    
async def testProxy(session, url, proxies, proxy, totalReviews):
    try:
        ip = proxy.find("td")
        proxy = "http://" + ip.text + ":" + ip.next_sibling.text
        response = await session.get(url, proxy=proxy, ssl=False, timeout=5)
        soup = BeautifulSoup(await response.text(), "html.parser")
        reviews = 0
        commaNum = soup.find(string=re.compile("total ratings, ")).text.split("ratings, ")[1].split(" ")[0].split(",")
        
        for index in range(len(commaNum)):
            reviews += int(commaNum[index]) * pow(1000, len(commaNum) - index - 1)
        if(reviews == totalReviews):
            print(reviews, " ", totalReviews, " ", proxy)
            proxies.append(proxy)
    except Exception as err:
        pass
        # DEBUG print(f"Error occured: {err}")