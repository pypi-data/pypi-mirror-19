
from bs4 import BeautifulSoup

def get_download_url(html, order_id):
    soup = BeautifulSoup(html, 'html.parser')
    captions = soup.find_all('caption')
    
    for cap in captions:
        if str(order_id) in cap.text:
            a = cap.find_next_sibling().find_next_sibling().find("a")
            return '/'.join(a['href'].split('/')[:-1])
