from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect,HttpResponse
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import re


def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        url = f'https://ahmia.fi/search/?q={search}'
        user_agent = UserAgent()
        headers = {'User-Agent': user_agent.random}
        res = requests.get(url, headers=headers)
        soup = bs(res.text, 'html.parser')
        result_listings = soup.select('ol.searchResults li')
        final_result = []
        for result in result_listings:
            result_title = result.find('cite')
            if result_title:
                result_title = result_title.text
            else:
                print("Sin Descripcion")   
            result_url = result.find('a')
            if result_url:
                result_url = result_url.text
            else:
                print("Titulo Desconocido")       
            result_desc = result.find('p').text
            final_result.append((result_url,result_title,  result_desc,))
         
        context = {
            'final_result': final_result,
            'search': search
        }

        return render(request, 'search.html', context)

    else:
        return render(request, 'search.html')


def onion_redirect(request):
    redirect_url = request.GET.get('redirect_url', '').replace('%22', '')
    redirect_url = redirect_url.replace('%26', '&').replace('%3F', '?')
    search_term = request.GET.get('search_term', '')

    if not redirect_url or not search_term:
        return HttpResponseBadRequest("Solicitud incorrecta: sin URL de parámetro GET ni término de búsqueda")

    if not redirect_url.startswith('http://') and not redirect_url.startswith('https://'):
        redirect_url = 'http://' + redirect_url

    domain = urlparse(redirect_url).netloc.lower()

    onion_re = re.compile(r'^[a-z2-7]{16,56}\.onion$')  

    if onion_re.match(domain):
        return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponseBadRequest("Solicitud incorrecta: esta no es una dirección de cebolla")
