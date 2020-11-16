from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()


class Db:

    def __init__(self):
        self.engine = create_engine('sqlite:///app.db', echo=False)

    def initialize(self):
        if not os.path.exists('app.db'):
            Base.metadata.create_all(self.engine)
        else:
            print("Db exists")

    def get_session(self):
        return Session(bind=self.engine)


db = Db()
