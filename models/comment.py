from models.base_model import BaseModel
from models.user import User
from models.post import Post
import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Comment(BaseModel):
    content = pw.TextField(null=False)
    post = pw.ForeignKeyField(Post, backref="comments", on_delete='CASCADE')