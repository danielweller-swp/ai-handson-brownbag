from bs4 import BeautifulSoup
import requests
  

def get_html_page(url):
    return requests.get(url).text

def get_html_page_text(url):
    return BeautifulSoup(get_html_page(url), features="html.parser").get_text()
