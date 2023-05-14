class Debug():
    """ help to develop project """

    @staticmethod
    def show_objects(_object):
        return [ method for method in dir(_object) if not method.startswith("_") ]