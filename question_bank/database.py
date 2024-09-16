import random
import re
import math
import os
import time
import traceback
import hashlib

from typing import List
from copy import deepcopy

from question_bank.models import (
    Base,
    Category,
    Subject,
    Question
)

from question_bank.exception import CategoryNotFoundError, SubjectNotFoundError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, subqueryload
from sqlalchemy.exc import OperationalError


# 資料庫連接字串
DATABASE_URL = os.environ.get("connectString")

# 建立引擎
engine = create_engine(DATABASE_URL)

retries = 5
while retries >= 0:
    try:
        # 建立模型
        Base.metadata.create_all(engine)
        break
    except OperationalError as e:
        if retries == 0:
            raise e
        print(f"連線失敗，重試中... ({retries} 次剩餘)")
        retries -= 1
        time.sleep(5)


# 建立連線階段
Session = sessionmaker(bind=engine)


class QuestionBank:

    @staticmethod
    def get_categorys() -> List[Category]:
        result = Session().query(Category).all()
        if result:
            return result
        else:
            raise CategoryNotFoundError()
    
    @staticmethod
    def get_subjects(*, category_id) -> List[Subject]:
        result = Session().query(Subject).filter_by(category_id=category_id).all()
        return result
    
    @staticmethod
    def get_subject(*, category_id, subject_id) -> Subject:
        result = Session().query(Subject).filter_by(category_id=category_id, subject_id=subject_id).first()
        if result:
            return result
        else:
            raise SubjectNotFoundError()
    
    @staticmethod
    def get_questions(*, category_id, subject_id) -> List[Question]:
        result = (Session().query(Question)
                  .options(
                      subqueryload(Question.category),
                      subqueryload(Question.subject).subqueryload(Subject.questions),
                      subqueryload(Question.options),
                      subqueryload(Question.answer),
                      subqueryload(Question.variables)
                    )
                  .filter_by(category_id=category_id)
                  .filter_by(subject_id=subject_id)).all()
        return result
    

class QuestionRandomizer:
    def __init__(self, question, random_seed):
        self.random_seed = random_seed
        self.question = deepcopy(question)
        self.seed_generator = random.Random(self.random_seed + int(hashlib.md5(self.question.content.encode()).hexdigest()[:10], 16)).random
        random.Random(self.seed_generator()).shuffle(self.question.options)

    def process_variables(self):
    
        def randint(a, b):
            return random.Random(self.seed_generator()).randint(a, b)

        def uniform(a, b):
            return random.Random(self.seed_generator()).uniform(a, b)

        def uniform_r(a, b, ndigits):
            return round(uniform(a, b), ndigits)

        def choice(seq):
            return random.Random(self.seed_generator()).choice(seq)

        safe_function = [
            "acos", "asin", "atan", "atan2", "ceil", "cos", "cosh", "degrees",
            "e", "exp", "fabs", "floor", "fmod", "frexp", "hypot", "ldexp",
            "log", "log10", "modf", "pi", "pow", "radians", "sin", "sinh",
            "sqrt", "tan", "tanh"
        ]
        safe_dict = dict([(f, getattr(math, f)) for f in safe_function])
        safe_dict.update(
            abs=abs,
            max=max,
            min=min,
            round=round,
            randint=randint,
            uniform=uniform,
            choice=choice,
            uniform_r=uniform_r
        )

        dangerous_keywords = ['__import__', 'eval', 'exec', 'open', 'os', 'sys', 'subprocess', '__']
        dangerous_chars = [';', '&', '|', '$', '`', '{', '}', '[', ']']
            
        for variable in self.question.variables:
            try:
                # 確認變數名稱符合命名規則 
                if not re.fullmatch(r"^(?!.*__)[a-zA-Z_][a-zA-Z0-9_]*$", variable.variable_name):
                    raise ValueError(f"Invalid variable name: '{variable.variable_name}'. Variable names must start with a letter or underscore, contain only letters, digits, or underscores, and must not contain double underscores '__'.")

                value = variable.variable_value

                # 替換或刪除危險關鍵字
                for keyword in dangerous_keywords:
                    value = re.sub(r'\b' + keyword + r'\b', '', value)
                
                # 刪除危險字符
                for char in dangerous_chars:
                    value = value.replace(char, '')

                # 禁止存取屬性
                value = re.sub(r'(?<!\d)\.(?!\d)', '', value)

                variable.variable_value = eval(value, {"__builtins__": None}, safe_dict)
            except (SyntaxError, NameError, TypeError):
                raise ValueError(f"Invalid variable value: '{variable.variable_value}'.")

        try:
            variable_map = dict((variable.variable_name, variable.variable_value) for variable in self.question.variables)
            
            self.question.content = self.question.content.format(**variable_map)

            for option in self.question.options:
                option.content = option.content.format(**variable_map)

        except (KeyError, ValueError):
            traceback.print_exc()