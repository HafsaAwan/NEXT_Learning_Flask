from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin

class StudentGuardian(BaseModel):
    student = pw.ForeignKeyField(User, on_delete='CASCADE')
    guardian = pw.ForeignKeyField(User, on_delete='CASCADE')