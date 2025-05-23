from exceptions.base import BaseError


class ServiceError(BaseError):
    pass

### auth exceptions ### 

class UserDoesNotExist(ServiceError):
    pass


class UserPasswordVerificationFailedError(ServiceError):
    pass

### book exceptions ###

class BookDoesNotExist(ServiceError):
    pass


class BookISBNAlreadyExists(BookDoesNotExist):
    pass
