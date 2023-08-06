class DSNotFoundException(Exception):
    def __init__(self, message=None):
        super(DSNotFoundException, self).__init__(message)


class DSInvalidInputException(Exception):
    def __init__(self, message=None):
        super(DSInvalidInputException, self).__init__(message)


class DSInvalidKeyException(Exception):
    def __init__(self, message=None):
        super(DSInvalidKeyException, self).__init__(message)
