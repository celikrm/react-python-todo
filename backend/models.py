from database import Base
from sqlalchemy import Column, Integer, String


# veritabanındaki tabloyu oluşturma
class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    content = Column(String)