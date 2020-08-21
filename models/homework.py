from models.base_model import BaseModel
from models.user import User
from models.student_classroom import StudentClassroom
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Homework(BaseModel):
    title = pw.CharField(unique=True, null=False)
    section = pw.ForeignKeyField(StudentClassroom, on_delete='CASCADE')
    file_path = pw.TextField(null=True)