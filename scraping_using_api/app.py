import requests
from fake_useragent import UserAgent
import json
import pprint
from urllib.parse import urljoin


all_products=[]
ua=UserAgent()
url = "https://www.walgreens.com/productsearch/v1/products/search"
headers = {
  'Content-Type': 'application/json',
  'User-Agent':ua.google
}

def scraper(page_number=1):

    payload = {"p":page_number,"s":24,"view":"allView","geoTargetEnabled":False,"abtest":["tier2","showNewCategories"],"deviceType":"desktop","id":["350006"],"requestType":"tier3","sort":"Top Sellers","couponStoreId":"15196"}

    response = requests.post(url, headers=headers, data = json.dumps(payload))

    data=response.json()

    try:
        products=data['products']

        for product in products:

            pr_info=product['productInfo']
            pr={
                'img':pr_info['imageUrl'],
                'price':pr_info['priceInfo']['regularPrice'],
                'id':pr_info['prodId'],
                'name':pr_info['productDisplayName'],
                'url':urljoin('https://www.walgreens.com',pr_info['productURL'])
            }
            all_products.append(pr)
        
        page_number+=1
        scraper(page_number)

    except KeyError:
        return None


scraper()
pprint.pprint(all_products)