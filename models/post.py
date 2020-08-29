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
    file_path = pw.TextField(null=True)

    @hybrid_property
    def full_file_path(self):
        if self.file_path:
            from app import app
            return app.config.get("S3_LOCATION") + self.file_path
        else:
            return ""