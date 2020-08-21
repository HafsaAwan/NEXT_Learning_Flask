from models.base_model import BaseModel
from models.user import User
from models.classroom import Classroom
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin


class StudentClassroom(BaseModel):
    student = pw.ForeignKeyField(User, on_delete='CASCADE')
    class_name = pw.ForeignKeyField(Classroom, on_delete='CASCADE')