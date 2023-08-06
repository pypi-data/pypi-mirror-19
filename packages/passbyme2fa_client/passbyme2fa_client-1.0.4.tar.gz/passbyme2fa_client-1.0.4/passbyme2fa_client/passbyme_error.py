class PassByMEError(BaseException):
    def __init__(self, response):
        self.response = response
