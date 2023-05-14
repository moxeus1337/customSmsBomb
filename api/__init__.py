import random

class Sms():
    THREADS_PER_PHONE = 1
    __PROXIES = None
    total_count = 0
    __usening_proxies = []

    @classmethod
    def configure(cls, thread_count, proxies):
        cls.THREADS_PER_PHONE = thread_count
        cls.__PROXIES = proxies

    @classmethod
    def random_select_proxy(cls):
        if cls.__PROXIES is None:
            return cls.__PROXIES
        rnd_proxy = random.choice(cls.__PROXIES)
        if not rnd_proxy in cls.__usening_proxies:
            dict_proxy = dict(rnd_proxy)
            cls.__usening_proxies.append(dict_proxy)
            return dict_proxy
        return cls.random_select_proxy()

    @classmethod
    def free_usening_proxy(cls, proxy):
        if proxy is not None:
            cls.__usening_proxies.remove(proxy)