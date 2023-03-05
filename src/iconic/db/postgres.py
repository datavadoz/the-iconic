from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Postgres:
    def __init__(self, host: str, username: str, password: str, db_name: str):
        self.engine = create_engine(f'postgresql://{username}:{password}@{host}/{db_name}')
        self.session = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False,
                         autoflush=False, expire_on_commit=False))

    def get(self, model_class, model_id):
        return self.session.query(model_class).get(model_id)

    def upsert_df(self, df, model_class):
        df.to_sql(schema='public', name=model_class.__tablename__,
                  con=self.engine, index=False, if_exists='append')
