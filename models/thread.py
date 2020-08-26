from models.base_model import BaseModel
from models.user import User
from models.course import Course
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Thread(BaseModel):
    course = pw.ForeignKeyField(Course, on_delete='CASCADE')
