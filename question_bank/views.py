from question_bank.database import QuestionBank

from django import http
from pydantic_core import to_jsonable_python

def category(request, category_id: int=None):
    result = None
    match request.method:
        case "GET":
            with QuestionBank() as question_bank:
                result = to_jsonable_python(question_bank.get_category(category_id=category_id))
        case _:
            return http.HttpResponseNotAllowed(["GET"])

    return http.JsonResponse(result, safe=False)

def subject(request, category_id: int, subject_id: int=None):
    result = None
    match request.method:
        case "GET":
            with QuestionBank() as question_bank:
                result = to_jsonable_python(question_bank.get_subject(category_id=category_id, subject_id=subject_id))
        case _:
            return http.HttpResponseNotAllowed(["GET"])

    return http.JsonResponse(result, safe=False)

def question(request, category_id: int, subject_id: int, question_id: int=None):
    result = None
    match request.method:
        case "GET":
            with QuestionBank() as question_bank:
                result = to_jsonable_python(question_bank.get_questions(
                    category_id=category_id, subject_id=subject_id, question_id=question_id)
                )
        case _:
            return http.HttpResponseNotAllowed(["GET"])
    
    return http.JsonResponse(result, safe=False)

def option(request, category_id: int, subject_id: int, question_id: int, option_id: int=None):
    result = None
    match request.method:
        case "GET":
            with QuestionBank() as question_bank:
                result = to_jsonable_python(question_bank.get_option(
                    category_id=category_id, subject_id=subject_id, question_id=question_id, option_id=option_id)
                )
        case _:
            return http.HttpResponseNotAllowed(["GET"])

    return http.JsonResponse(result, safe=False)
    
def answer(request, category_id: int, subject_id: int, question_id: int):
    result = None
    match request.method:
        case "GET":
            with QuestionBank() as question_bank:
                result = to_jsonable_python(question_bank.get_answer(
                    category_id=category_id, subject_id=subject_id, question_id=question_id)
                )
        case _:
            return http.HttpResponseNotAllowed(["GET"])

    return http.JsonResponse(result, safe=False)

def variable(request, category_id: int, subject_id: int, question_id: int):
    result = None
    match request.method:
        case "GET":
            with QuestionBank() as question_bank:
                result = to_jsonable_python(question_bank.get_variable(
                    category_id=category_id, subject_id=subject_id, question_id=question_id)
                )
        case _:
            return http.HttpResponseNotAllowed(["GET"])

    return http.JsonResponse(result, safe=False)