from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Course(BaseModel):
    title = pw.TextField(unique=True, null=False)
    teacher = pw.ForeignKeyField(User, backref="my_courses", on_delete='CASCADE')