class QuestionBankException(Exception):
    pass


class CategoryNotFoundError(QuestionBankException):
    pass


class SubjectNotFoundError(QuestionBankException):
    pass
