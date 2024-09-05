import random

from line_bot.utils.template import Template
from line_bot.utils.postback import QuestionPostback
from question_bank.database import QuestionBank, QuestionRandomizer

from linebot.v3.messaging.models import (
    FlexMessage, FlexCarousel
)

class TemplateBuilder:

    @staticmethod
    def select_category() -> FlexMessage:
        category_bubbles = []

        for category in QuestionBank.get_categorys():
            category_bubbles.append(Template.category_bubble(category))

        flex_message = FlexMessage(
            alt_text='題庫 | 選擇類科', 
            contents=FlexCarousel(contents=category_bubbles)
        )
        return flex_message
    
    @staticmethod
    def select_subject(postback: QuestionPostback) -> FlexMessage:
        subject_bubbles = []

        for subject in QuestionBank.get_subjects(category_id=postback.category_id):
            subject_bubbles.append(Template.subject_bubble(subject, postback))
        
        flex_message = FlexMessage(
            alt_text='題庫 | 選擇科目', 
            contents=FlexCarousel(contents=subject_bubbles)
        )
        return flex_message
    
    @staticmethod
    def select_mode(postback: QuestionPostback) -> FlexMessage:
        subject = QuestionBank.get_subject(category_id=postback.category_id, subject_id=postback.subject_id)
        bubble = Template.mode_bubble(subject, postback)

        flex_message = FlexMessage(
            alt_text='題庫 | 選擇科目', 
            contents=FlexCarousel(contents=[bubble])
        )
        return flex_message

    @staticmethod
    def question(postback: QuestionPostback) -> FlexMessage:

        questions = QuestionBank.get_questions(category_id=postback.category_id, subject_id=postback.subject_id)
        questions.sort(key=lambda q: q.question_id)

        if postback.question_index >= len(questions):
            return TemplateBuilder.question_result(postback)

        # shuffle questions
        random.Random(postback.question_seed).shuffle(questions)

        randomizer = QuestionRandomizer(questions[postback.question_index], postback.question_seed)
        randomizer.process_variables()

        question = randomizer.question

        bubble = Template.question_bubble(question, postback)

        flex_message = FlexMessage(
            alt_text='題庫 | 題目 {} / {}'.format(len(question.subject.questions), postback.question_index+1), 
            contents=FlexCarousel(contents=[bubble])
        )
        return flex_message
    
    @staticmethod
    def question_result(postback: QuestionPostback) -> FlexMessage:
        subject = QuestionBank.get_subject(category_id=postback.category_id, subject_id=postback.subject_id)

        bubble = Template.result_bubble(subject, postback)

        flex_message = FlexMessage(
            alt_text='題庫 | 結果 ', 
            contents=FlexCarousel(contents=[bubble])
        )
        return flex_message
    
    @staticmethod
    def question_review(postback: QuestionPostback) -> FlexMessage:
        incorrect_answers_index = [i for i, ans in enumerate(postback.reply_answer) if ans != "*"]

        questions = QuestionBank.get_questions(category_id=postback.category_id, subject_id=postback.subject_id)
        questions.sort(key=lambda q: q.question_id)

        # shuffle questions
        random.Random(postback.question_seed).shuffle(questions)
        question_index = incorrect_answers_index[0] if postback.question_index == 0 else postback.question_index

        next_question_index = incorrect_answers_index[(incorrect_answers_index.index(question_index) + 1) % len(incorrect_answers_index)]
        prev_question_index = incorrect_answers_index[(incorrect_answers_index.index(question_index) - 1) % len(incorrect_answers_index)]

        randomizer = QuestionRandomizer(questions[question_index], postback.question_seed)
        randomizer.process_variables()

        question = randomizer.question

        bubble = Template.review_bubble(question, question_index, next_question_index, prev_question_index, postback)

        flex_message = FlexMessage(
            alt_text='題庫 | 查看錯誤 ', 
            contents=FlexCarousel(contents=[bubble])
        )
        return flex_message