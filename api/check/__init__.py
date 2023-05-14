from utils import Utils

class Checker():
    """ check if sms api was successful """

    @staticmethod
    def status_code_check(response_obj, validate_code):
        status_code = response_obj.status_code    
        return validate_code == status_code

    @staticmethod
    def json_check(response_obj, validate_data, path):
        json_response = response_obj.json()
        response_data = Utils.select_by_path(json_response, path)
        return validate_data == response_data
        