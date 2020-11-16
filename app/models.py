from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import OperationalError
from app.database import db, Base
from PIL import Image
from io import BytesIO
import requests
from imagehash import average_hash


class Picture(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    hash_val = Column(String, nullable=False)
    link = Column(String, nullable=True)

    def __init__(self, link, path):
        self.link = link
        self.path = str(path)

    def initialize(self, lock, tolerance=7):
        image = Image.open(BytesIO(requests.get(self.link).content))
        self.hash_val = str(average_hash(image))
        with lock:
            if self.validate(tolerance):
                image.save(self.path)
                return True
        return False

    def validate(self, tolerance):
        session = db.get_session()
        try:
            pics = session.query(Picture).all()
            for p in pics:
                diff = abs(int(p.hash_val, 16) - int(self.hash_val, 16))
                if diff < tolerance:
                    print(f"Image {self.link} already in database (path: {p.path}, diff: {diff}, tolerance: {tolerance})")
                    return False
        except OperationalError:
            session.add(self)
            session.commit()
            return True
        session.add(self)
        session.commit()
        return True


db.initialize()




