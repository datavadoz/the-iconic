from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import scoped_session, sessionmaker


class Postgres:
    def __init__(self, host: str, username: str, password: str, db_name: str):
        self.engine = create_engine(f'postgresql://{username}:{password}@{host}/{db_name}')
        self.session = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False,
                         autoflush=False, expire_on_commit=False))

    def get(self, model_class, model_id):
        return self.session.query(model_class).get(model_id)

    def upsert_df(self, df, model_class, on_conflict_cols):
        insert_stmt = postgresql.insert(model_class).values(df.to_dict(orient='records'))
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=on_conflict_cols,
            set_={c.key: c for c in insert_stmt.excluded if c.key not in on_conflict_cols})
        self.session.execute(upsert_stmt)
        self.session.commit()

    def query(self, statement):
        return self.session.execute(statement).fetchall()
