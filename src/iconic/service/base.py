from iconic.db.postgres import Postgres


class BaseService:
    def __init__(self):
        self.db = Postgres('database', 'root', 'root', 'the-iconic')
