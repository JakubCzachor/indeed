#Bestbuy Price Scraper
#Input: Search Term
#Output: Array of search results along with price
#Packages: Requests for http get requests, BeautifulSoup for parsing


import requests
from bs4 import BeautifulSoup


searchTerm = input("Enter Search Term Here: ")
url = f'https://www.bestbuy.com/site/searchpage.jsp?st={searchTerm}'


headers = {
    'Referer': 'https://www.bestbuy.com/',
    'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
session = requests.Session()
session.headers.update(headers)


response = session.get(url, headers=headers)
res = []

#Successful Get Request
if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    #Finds all SKU's listed
    result_collection = soup.find_all('li', class_='sku-item')

    #Finds title & price
    for result in result_collection:
        title = result.find(class_='sku-title').get_text()
        price_div = result.find(class_='priceView-hero-price priceView-customer-price')

        if price_div:
            price = price_div.find('span', attrs={'aria-hidden': 'true'})

            #Not all items have price available w/o login/atc
            if price:
                price_text = price.get_text()
                res.append(f'{title.strip()} - {price_text.strip()}')
    #Results
    for item in res:
        print(item)
      
else:
    print(f"Failed to fetch: {response.status_code}")
