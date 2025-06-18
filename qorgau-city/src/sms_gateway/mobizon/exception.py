class MobizonApiException(Exception):
    def __init__(self, message="Mobizon API Exception"):
        self.message = message
        super().__init__(self.message)
