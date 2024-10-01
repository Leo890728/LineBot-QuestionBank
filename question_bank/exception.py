class QuestionBankException(Exception):
    pass


class CategoryNotFoundError(QuestionBankException):
    pass


class SubjectNotFoundError(QuestionBankException):
    pass


class QuestionNotFoundError(QuestionBankException):
    pass


class OptionNotFoundError(QuestionBankException):
    pass