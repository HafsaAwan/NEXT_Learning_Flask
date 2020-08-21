from models.base_model import BaseModel
from models.user import User
from models.thread import Thread
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Post(BaseModel):
    title = pw.CharField(null=False)
    content = pw.CharField(null=False)
    thread = pw.ForeignKeyField(Thread, on_delete='CASCADE')