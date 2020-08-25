from models.base_model import BaseModel
from models.user import User
from models.student_course import StudentCourse
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Assignment(BaseModel):
    title = pw.TextField(unique=True, null=False)
    course = pw.ForeignKeyField(StudentCourse, on_delete='CASCADE')
    file_path = pw.TextField(null=True)
    grade = pw.CharField(unique=True, null=True)