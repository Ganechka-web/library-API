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


class BookDoesNotHaveAnyInstancesError(ServiceError):
    """raises when reader trying to borrow book with 0 instances"""

### reader exceptions ###

class ReaderDoesNotExist(ServiceError):
    pass


class ReaderEmailAlreadyExists(ServiceError):
    pass

### borrowed_book exceptions ###

class BorrowedBookDoesNotExist(ServiceError):
    pass


class BorrowedBookAlreadyBorrowed(ServiceError):
    pass


class BorrowedBookCountPerReaderError(ServiceError):
    """raises when reader trying to borrow fouth book"""


class BorrowedBookInvalidReturnDateError(ServiceError):
    """raises when return_at is less than borrow_at date"""


class BorrowedBookUnableToBorrowBook(ServiceError):
    """raises when book instances is 0"""
    