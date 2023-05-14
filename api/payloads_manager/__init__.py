import json

class PayloadsManager():

    """ params.json rule decisiver
        METHODS tuple have to same order with params.json
        ALGORITHMS tuple have to same order with params.json """

    # target information specifiers represents
    __PARAMS_FILE_PATH = "./api/params.json"
    __PHONE_REPRESENT = "%%PHONE_NUMBER%%"
    __MAIL_REPRESENT = "%%MAIL_ADDRESS%%"

    # json and other selectors
    VALIDATE_DATA_SELECTOR = "validateData"
    VALIDATE_PATH_SELECTOR = "validatePath"
    METHOD_NAME_SELECTOR = "methodName"
    PAYLOAD_ARGS_SELECTOR = "payload"
    NAME_SELECTOR = "name"
    METHOD_SELECTOR = "method"
    ALGORITHM_SELECTOR = "algorithm"

    # methods list
    METHODS = ("post", "get", "put", "customMethods")
    MTD_POST, MTD_GET, MTD_PUT, MTD_CUSTOM = METHODS
    ALGORITHMS = ("json", "statusCode", "custom")
    ALG_JSON, ALG_STATUS_CODE, ALG_CUSTOM = ALGORITHMS 

    def __init__(self, phone, mail):
        self.phone = phone
        self.mail = mail
        self.confd_payloads = self.get_payloads()
        self.last_payload_name = self.confd_payloads[-1][self.NAME_SELECTOR]
    
    def get_payloads(self):
        with open(self.__PARAMS_FILE_PATH) as f:
            payloads_text = f.read()
        payloads = payloads_text.replace(self.__PHONE_REPRESENT, self.phone).replace(self.__MAIL_REPRESENT, self.mail)
        jsonize_payloads = json.loads(payloads)
        listed_payloads = self.select_algorithm_dicts(jsonize_payloads)
        return listed_payloads

    @classmethod
    def select_algorithm_dicts(cls, data):
        results = []
        for method, algorithms in data.items():
            for algorithm, dicts in algorithms.items():
                for dictionary in dicts:
                    dictionary[cls.METHOD_SELECTOR] = method
                    dictionary[cls.ALGORITHM_SELECTOR] = algorithm
                    results.append(dictionary)
        return results