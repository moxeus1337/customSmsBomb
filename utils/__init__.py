import random
import string
import os

class Utils():
    """ make some calculations for project """

    # const values for fake email
    __EMAIL_DOMAIN_NAME = "@gmail.com"
    __EMAIL_LENGTH = 19

    # return random mail else return mail 
    @classmethod
    def mail_generator(cls):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(cls.__EMAIL_LENGTH))+cls.__EMAIL_DOMAIN_NAME

    # return wanted data from a dict using specific path like "key1.key2.key3"
    @staticmethod
    def select_by_path(data, path):
        keys = path.split(".")
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    @staticmethod
    def check_file(arg, path):
        if "./"+arg == path: 
            return os.path.exists(path)