import requests
from lxml import html
import json

def write_to_json(filename,data):
    with open(filename,mode='w') as my_file:
        json_data=json.dumps(data)
        my_file.write(json_data)

response=requests.get(url='https://www.ebay.com/trending',headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'})

tree=html.fromstring(response.text)
trending_product_info_list=[]
trending_products=tree.xpath('//div[contains(@id,"topic")]/div[@class="topic-container"]')

for product in trending_products:

    a_path='.//h2[@class="title"]/a'
    title=product.xpath(a_path+'/text()')[0]
    url=product.xpath(a_path+'/@href')[0]
    description=product.xpath('.//div[@class="info"]/p/text()')[0]
    searches=product.xpath('.//div[@class="graph"]/descendant::div[@class="views"]/strong/text()')[0]
    product_info={'title':title,
                'url':url,
                'description':description,
                'searches':searches}
    trending_product_info_list.append(product_info)

write_to_json('trending.json',trending_product_info_list)


