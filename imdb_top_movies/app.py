import requests
from lxml import html
from urllib.parse import urljoin
from pymongo import MongoClient


all_movies=[]

def insert_to_db(movie_list):
    conn=MongoClient(host='mongodb://sadkirat:khalsapanth@cluster0-shard-00-00-radmq.mongodb.net:27017,cluster0-shard-00-01-radmq.mongodb.net:27017,cluster0-shard-00-02-radmq.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db=conn['currencies']
    col=db['movies']
    for movie in movie_list:
        exists=col.find_one({'title':movie['title']})
        if exists:
            if(exists['rating']!=movie['rating']):
                col.replace_one({'title':movie['title']},movie)
        else:
            col.insert_one(movie)

def scrape(url):
    response=requests.get(url=url,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'})

    tree=html.fromstring(response.content)
    my_movie_list=tree.xpath('//div[@class=\'lister-list\']/div[contains(@class,\'lister-item\')]/div[contains(@class,\'content\')]')
    for movie in my_movie_list:
        movie_dict={
            'title':movie.xpath('.//h3/a/text()')[0],
            'year':movie.xpath('.//h3/span[2]/text()')[0].strip('()'),
            'duration':movie.xpath('.//p[1]/span[@class=\'runtime\']/text()')[0],
            'rating':movie.xpath('.//div/div/@data-value')[0],
        }
        all_movies.append(movie_dict)
    next_page=tree.xpath('//div[@class=\'nav\']/div[2]/a[contains(@class,\'next-page\')]/@href')
    if(len(next_page)!=0):
        url=urljoin(url,next_page[0])
        scrape(url)



scrape(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc&ref_=adv_prv')
print(all_movies)
insert_to_db(all_movies)