from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Classroom(BaseModel):
    title = pw.CharField(unique=True, null=False)
    teacher = pw.ForeignKeyField(User, on_delete='CASCADE')