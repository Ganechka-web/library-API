from exceptions.base import BaseError


class RepositoryError(BaseError):
    pass


class RowDoesNotExist(RepositoryError):
    pass
