from bs4 import BeautifulSoup

class CustomChecker():

    """ check if sms api was successful for custom apis """
    
    __PARSER = "html.parser"
    CUSTOM_CHECK_FUNC_REPRESENT = "_custom_check"

    def __init__(self, phone, mail):
        # add phone and mail access because 
        # if adding a new sms api needs to use custom control 
        # if this control function needs sms sent phone number or e-mail address
        self.phone = phone
        self.mail = mail

    @staticmethod
    def kahvedunyasi_custom_check(response_obj):
        message = response_obj.json()["meta"]["messages"]["error"]
        if len(message) == 0:
            return True

    @classmethod
    def dsmartgo_custom_check(cls, response_obj):
        html = response_obj.text
        
        try:
            BeautifulSoup(html, cls.__PARSER).find("div", {"class": "info-text"}).text.strip()
        except AttributeError:
            return True
        
        return False

    @staticmethod
    def pinar_custom_check(response_obj):
        html = response_obj.text
        if html == "true":
            return True

    @staticmethod
    def ebebek_custom_check(response_obj):
        status = response_obj.json()["status"]
        if status == "SUCCESS":
            return True

    @staticmethod
    def gratis_custom_check(response_obj):
        status_code = response_obj.status_code
        if status_code == 200:
            return True
