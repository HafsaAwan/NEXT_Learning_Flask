from models.base_model import BaseModel
from models.user import User
from models.course import Course
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin


class StudentCourse(BaseModel):
    student = pw.ForeignKeyField(User, on_delete='CASCADE')
    course_name = pw.ForeignKeyField(Course, on_delete='CASCADE')