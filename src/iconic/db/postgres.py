from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Postgres:
    def __init__(self, host: str, username: str, password: str, db_name: str):
        self.uri = f'postgresql://{username}:{password}@{host}/{db_name}'
        self.session = scoped_session(
            sessionmaker(bind=create_engine(self.uri),
                         autocommit=False, autoflush=False, expire_on_commit=False))

    def get(self, model_class, model_id):
        return self.session.query(model_class).get(model_id)
