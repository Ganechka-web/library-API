from exceptions.base import BaseError


class ServiceError(BaseError):
    pass


class UserDoesNotExist(ServiceError):
    pass


class UserPasswordVerificationFailedError(ServiceError):
    pass
