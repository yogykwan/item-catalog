from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime, Text
from datetime import datetime
from base import Base


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, Sequence('item_id'), primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    highlight = Column(Text, default="")
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name, 'url': self.url, 'highlight': self.highlight,
                'category_id': self.category_id, 'user_id': self.user_id}
