from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base


class BaseModel:
    @classmethod
    def get_schema_dict(cls):
        inspections = inspect(cls)
        schema_dict = {column.name: column.type.python_type for column in inspections.c}
        return schema_dict


Base = declarative_base(cls=BaseModel)
