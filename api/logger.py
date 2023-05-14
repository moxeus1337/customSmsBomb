from colorama import Fore, init
init()

from api import Sms

class Logger(Sms):
    """ log result of sent sms """

    @staticmethod
    def print_result(result, api_domain, phone, rnd_proxy, self_count):

        if result:
            message = f"{Fore.GREEN}Başarılı{Fore.WHITE} | {Fore.GREEN}Kişiye Gönderilen -> {self_count}{Fore.WHITE} | {Fore.GREEN}Total -> {Sms.total_count}{Fore.WHITE} | Proxy -> {Fore.LIGHTMAGENTA_EX}{rnd_proxy}{Fore.WHITE} | Site -> {Fore.YELLOW}{api_domain}"
        else:
            message = f"{Fore.RED}Başarısız{Fore.WHITE} | Proxy | {Fore.LIGHTMAGENTA_EX}{rnd_proxy}{Fore.WHITE} | Site -> {Fore.YELLOW}{api_domain}"
 
        print(message)
