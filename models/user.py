from models.base_model import BaseModel
from models.role import Role
import peewee as pw
from playhouse.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin


class User(UserMixin, BaseModel):
    first_name = pw.CharField(null=False)
    last_name = pw.CharField(null=False)
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password_hash = pw.TextField(null=False)
    password = None
    image_path = pw.TextField(null=True)
    role = pw.ForeignKeyField(Role, on_delete='CASCADE')
    about_me = pw.TextField(null=True)
    fav_quote=pw.TextField(null=True)


    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            from app import app
            return app.config.get("S3_LOCATION") + "new_default_picture.png"

    def validate(self):
        # Email should be unique
        existing_user_email = User.get_or_none(User.email==self.email)
        if existing_user_email and existing_user_email.id != self.id:
            self.errors.append(f"User with email {self.email} already exists!")
        # Username should be unique
        existing_user_username = User.get_or_none(User.username==self.username)
        # also check if current userid is not same as the newly created user so we can update details
        if existing_user_username and existing_user_username.id != self.id:
            self.errors.append(f"User with username {self.username} already exists!")
        
        # Password should be longer than 6 characters
        if self.password:
            if len(self.password) <= 6:
                self.errors.append("Password is less than 6 characters")
            # Password should have both uppercase and lowercase characters
            # Password should have at least one special character (REGEX comes in handy here)
            has_lower = re.search(r"[a-z]", self.password)
            has_upper = re.search(r"[A-Z]", self.password)
            has_special = re.search(r"[\[ \] \* \$ \% \^ \& \# \@ \? ]", self.password)

            if has_lower and has_upper and has_special:
                self.password_hash = generate_password_hash(self.password)
            else:
                self.errors.append("Password either does not have upper, lower or special characters!")