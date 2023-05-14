import requests

class ProxyDownloader():

    @staticmethod
    def proxy_scrape_com():
        API_URL = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        response = requests.get(API_URL)
        proxy_list =  response.text.strip().split("\n")
        return proxy_list