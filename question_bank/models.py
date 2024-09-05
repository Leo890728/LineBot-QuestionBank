from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


# 建立基類
Base = declarative_base()

# 定義 ORM 模型
class Category(Base):
    __tablename__ = 'Category'
    category_id = Column("CategoryID", Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("Name", String(16), nullable=False)
    background_image = Column("BackgroundImage", String(256), nullable=True)

    subjects = relationship("Subject", back_populates="category")
    questions = relationship("Question", back_populates="category")

    def __repr__(self):
        return "<Category(CategoryID={category_id}, Name={name})>".format(
            category_id=self.category_id,
            name=self.name
        )

class Subject(Base):
    __tablename__ = 'Subject'
    subject_id = Column("SubjectID", Integer, primary_key=True, autoincrement=True, nullable=False)
    category_id = Column("CategoryID", ForeignKey("Category.CategoryID"), nullable=False)
    name = Column("Name", String(16), nullable=False)
    description = Column("Description", String(32), nullable=False)
    background_image = Column("BackgroundImage", String(256), nullable=True)

    category = relationship("Category", back_populates="subjects")
    questions = relationship("Question", back_populates="subject")

    def __repr__(self):
        return "<Subject(CategoryID={category_id}, SubjectID={subject_id}, Name={name})>".format(
            category_id=self.category_id,
            subject_id=self.subject_id,
            name=self.name
        )

class Question(Base):
    __tablename__ = "Question"
    question_id = Column("QuestionID", Integer, primary_key=True, autoincrement=True, nullable=False)
    category_id = Column("CategoryID", ForeignKey("Category.CategoryID"), nullable=False)
    subject_id = Column("SubjectID", ForeignKey("Subject.SubjectID"), nullable=False)
    content = Column("Content", String(256), nullable=False)

    category = relationship("Category", back_populates="questions")
    subject = relationship("Subject", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")
    answer = relationship("QuestionAnswer", back_populates="question")
    variables= relationship("QuestionVariable", back_populates="question")

    def __repr__(self):
        return "<Question(CategoryID={category_id}, SubjectID={subject_id}, QuestionID={question_id}, Content={content})>".format(
            category_id=self.category_id,
            subject_id=self.subject_id,
            question_id=self.question_id,
            content=self.content[:10]
        )

class QuestionOption(Base):
    __tablename__ = "QuestionOption"
    option_id = Column("OptionID", Integer, primary_key=True, nullable=False)
    question_id = Column("QuestionID", ForeignKey("Question.QuestionID"), primary_key=True, nullable=False)
    content = Column("Content", String(256), nullable=False)

    question = relationship("Question", back_populates="options")

    def __repr__(self):
        return "<QuestionOption(QuestionID={question_id}, OptionID={option_id}, Content={content})>".format(
            question_id=self.question_id,
            option_id=self.option_id,
            content=self.content
        )

class QuestionAnswer(Base):
    __tablename__ = "QuestionAnswer"
    question_id = Column("QuestionID", ForeignKey("Question.QuestionID"), primary_key=True, nullable=False)
    option_id = Column("OptionID", ForeignKey("QuestionOption.OptionID"), primary_key=True, nullable=False)

    question = relationship("Question", back_populates="answer")

    def __repr__(self):
        return "<QuestionAnswer(QuestionID={question_id}, OptionID={option_id})>".format(
            question_id=self.question_id,
            option_id=self.option_id
        )

class QuestionVariable(Base):
    __tablename__ = "QuestionVariable"
    question_id = Column("QuestionID", ForeignKey("Question.QuestionID"), primary_key=True, nullable=False)
    variable_name = Column("VariableName", String(16), primary_key=True, nullable=False)
    variable_value = Column("VariableValue", String(64), nullable=False)

    question = relationship("Question", back_populates="variables")

    def __repr__(self):
        return "<QuestionVariable(QuestionID={question_id}, VariableName={variable_name}, VariableValue={variable_value})>".format(
            question_id=self.question_id,
            variable_name=self.variable_name,
            variable_value=self.variable_value
        )