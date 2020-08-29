from models.base_model import BaseModel
from models.user import User
from models.thread import Thread
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Post(BaseModel):
    post_content = pw.TextField(null=False)
    thread = pw.ForeignKeyField(Thread, on_delete='CASCADE')
    user = pw.ForeignKeyField(User, backref="posts", on_delete='CASCADE')