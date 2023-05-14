from requests.exceptions import RequestException
import argparse
from colorama import Fore

from utils import Utils
from api.proxy_manager import ProxyManager

class Validation():
    """ validate and generate the values entered by the user """

    __PHONE_LENGTH = 10
    __VICTIMS_LIST_FILE_PATH = "./victims.txt"
    __SORTED_VICTIMS = (0, 1, 2)
    __PHONE, __MAIL, __COUNT = __SORTED_VICTIMS
    __PROXY_ARG_SEP = ":"


    # if entered phone number is wrong raise ArgumentError else return phone number
    @classmethod   
    def phone_checker(cls, phone_or_file):
        if Utils.check_file(phone_or_file, cls.__VICTIMS_LIST_FILE_PATH):
            with open(cls.__VICTIMS_LIST_FILE_PATH) as f:
                phones = tuple(line.strip().split()[cls.__PHONE] for line in f.readlines())
            return phones
        phone_length = len(phone_or_file)
        if phone_length != cls.__PHONE_LENGTH:
            print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz." + Fore.RESET)
            raise argparse.ArgumentTypeError("Yanlış Numara")
        return (phone_or_file,)

    # if mail is not correct raise ArgumentError
    @classmethod
    def mail_checker(cls, mail_or_file):
        if Utils.check_file(mail_or_file, cls.__VICTIMS_LIST_FILE_PATH):
            with open(cls.__VICTIMS_LIST_FILE_PATH) as f:
                lines = f.readlines()
                mails = tuple(str(line.strip().split()[cls.__MAIL]) if line.strip().split()[cls.__MAIL] != "*" else Utils.mail_generator() for line in lines)
            return mails
        if ("@" not in mail_or_file or ".com" not in mail_or_file) and mail_or_file != "":
            raise argparse.ArgumentTypeError("Yanlış email")
        return (mail_or_file,)

    @classmethod
    def count_checker(cls, count_or_file):
        if Utils.check_file(count_or_file, cls.__VICTIMS_LIST_FILE_PATH):
            with open(cls.__VICTIMS_LIST_FILE_PATH) as f:
                counts = tuple(int(line.strip().split()[cls.__COUNT]) for line in f.readlines())
            return counts
        return int(count_or_file)

    @classmethod
    def proxy_checker(cls, proxy):
        splitted_args = proxy.split(cls.__PROXY_ARG_SEP)
        proxy_file_or_name = splitted_args[0]
        proxy_type = splitted_args[-1]
        if not proxy_type.strip() or not cls.__PROXY_ARG_SEP in proxy or len(splitted_args) != 2:
            raise argparse.ArgumentTypeError("Lütfen proxy tipini belirtiniz. (proxies.txt:type)")
        if proxy_file_or_name in ProxyManager.PROXIES:
            try:
                ProxyManager.get_proxies(proxy_file_or_name)
            except RequestException:
                raise argparse.ArgumentTypeError("Proxy listesi indirilemedi.")
        proxies = ProxyManager.read_proxies(proxy_type)
        if not proxies:
            raise argparse.ArgumentTypeError("Proxy dosyasında proxy bulunmamaktadır.")
        return proxies