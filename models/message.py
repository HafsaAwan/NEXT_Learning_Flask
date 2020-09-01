from models.base_model import BaseModel
from models.user import User

import peewee as pw
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin

class Message(BaseModel):
    message = pw.TextField(null=False)
    from_user = pw.ForeignKeyField(User, backref="my_messages", on_delete='CASCADE')
    to_user = pw.ForeignKeyField(User, backref="my_messages", on_delete='CASCADE')
    