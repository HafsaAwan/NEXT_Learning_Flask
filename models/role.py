from models.base_model import BaseModel
import peewee as pw

class Role(BaseModel):
    role = pw.TextField(unique=True)