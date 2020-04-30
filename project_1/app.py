import requests
from lxml import html
import json
import csv
import click


def write_to_json(filename, data):
    with open(filename, mode='w') as my_json:
        json_data = json.dumps(data)
        my_json.write(json_data)


def write_to_csv(filename, data):
    headers = ['title', 'price', 'availability', 'description']
    with open(filename, mode='w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=headers)
        csvwriter.writeheader()
        csvwriter.writerow(data)

@click.command()
@click.option('--book_url',default="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
              help='Please provide a book url')
@click.option('--filename',default="output.json",help='Please enter a filename(CSV/JSON)')

def scrape(book_url, filename):
    response = requests.get(book_url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})
    tree = html.fromstring(response.text)
    product_main = tree.xpath('//div[contains(@class,"product_main")]')[0]
    title = product_main.xpath('.//h1/text()')[0]
    price = product_main.xpath('.//p[1]/text()')[0]
    availability = product_main.xpath('.//p[2]/text()')[1].strip()
    in_stock = ''.join(list(filter(lambda x: x.isdigit(), availability)))
    description = tree.xpath(
        '//div[@id="product_description"]/following-sibling::p/text()')[0]

    book_info = {
        'title': title,
        'price': price,
        'availability': in_stock,
        'description': description,
    }

    extension=filename.split('.')[1]
    if extension=='csv':
        write_to_csv(filename,book_info)
    elif extension=='json':
         write_to_json(filename,book_info)
    else:
        click.echo("Extension not supported!")
    click.echo("success!!")

if __name__=='__main__':
    scrape()