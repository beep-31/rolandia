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
        def __init__(self, title, price, link, img):
            self.title = title
            if '£' in price:
                price = price.split('£')
                self.price = float(price[1])
            elif ('\xa0' in price):
                price = price.split('\xa0')[0].replace(',','.')
                price = float(price)
            self.link = link
            self.img = img
        def __str__(self):
            return f"Product Name:{self.title}, price: {self.price} \n Product link: {self.link} \n Product image: {self.img}"
        def __repr__(self):
            return repr((self.title, self.price))
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 OPR/68.0.3618.165'
    ZALANDO_LINK = 'https://www.zalando.es/catalogo/?q={}'
    DEFSHOP_LINK = 'https://en.def-shop.com/index.php?rf=2&search={}'
    ASOS_LINK = 'https://www.asos.com/search/?q={}'

    if request.method == 'GET':
        user_search = request.GET['productSearch']
    else:
        user_search = request.POST['productSearch']

    asos_final_url = ASOS_LINK.format(quote_plus(user_search))
    zalando_final_link = ZALANDO_LINK.format(quote_plus(user_search))
    defshop_final_link = DEFSHOP_LINK.format(quote_plus(user_search))
    headers = {'user-agent': USER_AGENT}
    response_asos = requests.get(asos_final_url, headers = headers)
    if response_asos.status_code == 200:
        asos_soup = bs(response_asos.content, 'html.parser')
    print(response_asos.status_code)
    return render(request, template_name='index.html')