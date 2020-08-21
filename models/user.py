from models.base_model import BaseModel
from models.role import Role
import peewee as pw
from playhouse.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin


class User(UserMixin, BaseModel):
    name = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True)
    password_hash = pw.TextField(null=False)
    password = None
    profile_image = pw.TextField(null=True)
    role = pw.ForeignKeyField(Role, on_delete='CASCADE')