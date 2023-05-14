import argparse
import warnings
import math
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

from utils.validation import Validation
from utils import Utils

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--phones", required=True, type=Validation.phone_checker, help="Sms gönderilecek numara veya liste dosyası.")
parser.add_argument("-m", "--mails", required=False, type=Validation.mail_checker, default=None, help="Mail gönderilecek mail ceya liste dosyası")
parser.add_argument("-c", "--count", required=False, type=Validation.count_checker, default=math.inf, help="Gönderilecek sms sayısı veya liste dosyası")
parser.add_argument("-x", "--proxy", required=False, type=Validation.proxy_checker, default=None, help="Proxy dosya ismi veya indirme site ismi")
parser.add_argument("-th", "--thread", required=False, type=int, default=1, help="Telefon başına düşen thread sayısı")
args = parser.parse_args()
controlled_mails = args.mails if args.mails is not None else tuple(Utils.mail_generator() for i in range(len(args.phones))) 
args.mails = controlled_mails

# main program start here
import threading
import os

from api import Sms
from api.api_client import ApiClient

def main():
    Sms.configure(args.thread, args.proxy)

    CLIs = []
    for index in range(len(args.phones)):
        phone = args.phones[index]
        mail = args.mails[index]
        count_limit = args.count
        if not isinstance(args.count, int) and args.count != math.inf:
            count_limit = args.count[index]
        CLI = ApiClient(phone, mail, count_limit)
        CLIs.append(CLI)

    worker_threads = []
    for CLI in CLIs:
        thread = threading.Thread(target=CLI.worker, daemon=True)
        worker_threads.append(thread)
        thread.start()

    for thread in worker_threads:
        thread.join()
    
    os._exit(1)

if __name__ == "__main__":
    main()
