from api.proxy_manager.proxy_downloader import ProxyDownloader

class ProxyManager():

    """Every proxy api func must return a proxy list. Not str.
       This class preparese proxies list for smsbomb. Like ProxyDownloader.
       Not managing proxylist when SmsBombing."""

    PROXY_LIST_FILE_PATH = "./proxies.txt"
    PROXIES = {
        "pxscrape": "proxy_scrape_com"
    }

    @classmethod
    def get_proxies(cls, proxy_name):
        scrape_func_name = cls.PROXIES.get(proxy_name, False)
        if scrape_func_name:
            scrape_func = getattr(ProxyDownloader, scrape_func_name)
            proxy_list = scrape_func()
            with open(cls.PROXY_LIST_FILE_PATH, "w") as f:
                f.writelines(proxy_list)
            return proxy_list
        
    @classmethod
    def read_proxies(cls, proxy_type):
        with open(cls.PROXY_LIST_FILE_PATH) as f:
            # use set for removing duplicates from proxies and reconvert it to list for work with random.choice
            proxies = list(set(frozenset({"http": f"{proxy_type}://{proxy_.strip()}"}.items()) for proxy_ in f.readlines()))
        return proxies
