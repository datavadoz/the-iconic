from sqlalchemy import Column, String

from iconic.model.base import Base


class Resource(Base):
    __tablename__ = 'resource'
    resource_name = Column(String, primary_key=True)
    resource_url = Column(String)
    resource_password = Column(String)
