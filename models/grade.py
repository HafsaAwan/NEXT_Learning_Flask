from models.base_model import BaseModel
from models.user import User
from models.student_course import StudentCourse
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Grade(BaseModel):
    grade = pw.CharField(unique=True, null=True)