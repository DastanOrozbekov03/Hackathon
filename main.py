import requests
from bs4 import BeautifulSoup as bs
import csv  

def write_to_csv(data):
    with open('kivano_nouts.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow((data['title'], data['price'], data['photo']))

def get_html(url):
    responce = requests.get(url)
    return responce.text


def get_total_page(html):
    soup = bs(html, 'lxml')
    page_ul = soup.find('div', class_='pager-wrap').find('ul')
    last_page = page_ul.find_all('li')[-1]
    total_page = last_page.find('a').get('href').split('=')[-1]
    return int(total_page)


def get_page_data(html):
    soup = bs(html, 'lxml')
    product_list = soup.find('div', class_='product-index product-index oh').find('div', class_='list-view')
    products = product_list.find_all('div', class_='item product_listbox oh')

    for product in products:
        try:
            photo = product.find('div', class_='listbox_img pull-left').find('a').find('img').get('src')
            
        except:
            photo = 'asdfghj'
        
        try:
            title = product.find('div', class_='listbox_title oh').find('a').text
            
        except:
            title = ''

        try:
            price = product.find('div', class_= 'listbox_price text-center').find('strong').text
            
        except:
            price = ''

        data = {'title': title, 
                'price': price, 
                'photo': photo }
        write_to_csv(data)


def main():
    url = 'https://www.kivano.kg/noutbuki'
    pages = '?page='
    
    total_pages = get_total_page(get_html(url))
    
    for page in range(1, total_pages+1):
        url_with_page = url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)

with open('kivano_nouts.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['title', 'price', 'photo'])

main()
