from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    public_id = Column(String(500), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(500), nullable=False)

    @property
    def serialize(self):
        data = {'id': self.id, 'public_id': self.public_id, 'username': self.username,\
                'email': self.email, 'password': self.password}
        return data
