# status_code 400 401 404
class BadRequestException(Exception):
    def __init__(self, message: str, code: int = 400, *args):
        super().__init__(*args)
        self.message = message
        self.code = code


class UnauthorizedException(Exception):

    def __init__(self, message: str, code: int = 401, *args):
        super().__init__(*args)
        self.message = message
        self.code = code


class NotFoundException(Exception):

    def __init__(self, message: str, code: int = 404, *args):
        super().__init__(*args)
        self.message = message
        self.code = code


class OkException(Exception):
    def __init__(self, message: str, code: int = 200, *args):
        super().__init__(*args)
        self.message = message
        self.code = code


__all__ = ["NotFoundException", "BadRequestException", "UnauthorizedException"]
