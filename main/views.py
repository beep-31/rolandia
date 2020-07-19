from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as bs 
import requests
from operator import itemgetter, attrgetter, methodcaller
from requests.compat import quote_plus

# Create your views here.

def home(request):
    return render(request, template_name='home.html')

@csrf_exempt
def search(request):
    class Product:
        def __init__(self, title, price, link, img, site):
            self.title = title
            if 'desde' in price:
                price = price.split('desde')
                price = price[1]
            if '€' in price:
                price = price.split('€')
                price = price[0].replace(',','.')
                self.price = float(price)
            elif ('\xa0' in price):
                price = price.split('\xa0')[0].replace(',','.')
                price = float(price)
                self.price = float(price)
            else:
                self.price = float(price)
            self.link = link
            self.img = img
            self.site = site
        def __str__(self):
            return f"Product Name:{self.title}, price: {self.price} \n Product link: {self.link} \n Product image: {self.img}"
        def __repr__(self):
            return repr((self.title, self.price))
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 OPR/68.0.3618.165'
    ZALANDO_LINK = 'https://www.zalando.es/catalogo/?q={}'
    LINK = 'https://www.zalando.es'
    DEFSHOP_LINK = 'https://def-shop.es/index.php?rf=2&search={}'
    ASOS_LINK = 'https://www.asos.com/es/search/?q={}'
    site_asos = 'ASOS'
    site_zalando = 'ZALANDO'
    site_defshop = 'DEFSHOP'
    if request.method == 'GET':
        user_search = request.GET.get('productSearch', False)
        sortType = request.GET.get('sortType', False)
        print(sortType)
        asos_final_url = ASOS_LINK.format(quote_plus(user_search))
        zalando_final_link = ZALANDO_LINK.format(quote_plus(user_search))
        defshop_final_link = DEFSHOP_LINK.format(quote_plus(user_search))
        results = []
        headers = {'user-agent': USER_AGENT}
        response_asos = requests.get(asos_final_url, headers = headers)
        #asos scrapper
        if response_asos.status_code == 200:
            asos_soup = bs(response_asos.content, 'html.parser')
            for a in asos_soup.find_all('article', class_='_2qG85dG'):
                anchor = a.find('a', class_='_3TqU78D')
                if anchor:
                    title = a.find('div', class_='_3J74XsK').text
                    link = anchor['href']
                    img = a.find('img').get('src')
                    if img == None:
                        img = 'static/img/no_image.png'
                paragraphs = asos_soup.find_all('p', class_='_1ldzWib')
                if paragraphs:
                    if a.find('span', class_='_3VjzNxC'):
                        price = a.find('span', class_='_3VjzNxC').text
                    else:
                        price = a.find('span', class_='_16nzq18').text                
                item = Product(title, price, link, img, site_asos)
                results.append(item)
        response_zalando = requests.get(zalando_final_link, headers = headers)
        if response_zalando.status_code == 200:
            #zalando scrapper
            zalando_soup = bs(response_zalando.content, 'html.parser')
            for div in zalando_soup.find_all('div', class_='cat_cardWrap-2UHT7'):
                a = div.find('a', class_='cat_imageLink-OPGGa')['href']
                link = LINK + a 
                img = div.find('img', class_='cat_image-1byrW')['src']
                if img == None:
                    img = 'static/img/no_image.png'
                title = div.find('div', class_='cat_articleName--arFp cat_ellipsis-MujnT').text
                if div.find('div', class_='cat_promotionalPrice-3GRE7'):
                    price = div.find('div', class_='cat_promotionalPrice-3GRE7').text
                else:
                    price = div.find('div', class_='cat_originalPrice-2Oy4G').text
                item = Product(title, price, link, img, site_zalando)
                results.append(item)
        response_defshop = requests.get(defshop_final_link, headers = headers)
        if response_defshop.status_code == 200:
            #defshop scrapper
            defshop_soup = bs(response_defshop.content, 'html.parser')
            for a in defshop_soup.find_all('article', class_=''):
                link = a.find('a')['href']
                price = a.find('div', class_='product-price').text
                price = price.split('€')[1].replace(',','.')
                title = a.find('div', class_='product-cat').text
                img = a.find('img').get('data-retina')
                if img == None:
                    img = 'static/img/no_image.png'
                img = img.split('f=auto/')[-1]
                item = Product(title,price,link,img,site_defshop)
                results.append(item)
        if sortType == 'relevance':
            return render(request, template_name='index.html', context = {"results":results,"total":len(results), "search":user_search})
        elif sortType == 'priceIncreasing':
            results = sorted(results, key=attrgetter('price'), reverse=False)
            return render(request, template_name='index.html', context = {"results":results,"total":len(results), "search":user_search})
        elif sortType == 'priceDecreasing':
            results = sorted(results, key=attrgetter('price'), reverse=True)
            return render(request, template_name='index.html', context = {"results":results,"total":len(results), "search":user_search})
        else:
            return render(request, template_name='index.html', context = {"results":results,"total":len(results), "search":user_search})
            