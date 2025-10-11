from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float
from sqlalchemy.orm import declarative_base
from typing import Any

Base = declarative_base()


class MovieDBModel(Base):
    """
    Модель фильма в базе данных
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    rating = Column(Float)
    genre_id = Column(Integer)
    created_at = Column(DateTime)

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'imageUrl': self.image_url,
            'location': self.location,
            'published': self.published,
            'rating': self.rating,
            'genreId': self.genre_id,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}, price={self.price})>"
