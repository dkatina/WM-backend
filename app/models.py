#Where I will initialize SQLAlchemy and create my models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, Integer, String, ForeignKey
from datetime import date

#Create Base Model to be inherited from
class Base(DeclarativeBase):
    pass

#Instatiate db and set Base model
db = SQLAlchemy(model_class=Base)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    role: Mapped[str] = mapped_column(String(360), nullable=False, default='user')
    spotify_id: Mapped[str] = mapped_column(String(360), nullable=True)

    collections: Mapped[list['Collection']] = relationship('Collection', back_populates='user')


class Collection(Base):
    __tablename__ = 'collections'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)
    cover_art: Mapped[str] = mapped_column(String(500), nullable=False)
    spotify_link: Mapped[str] = mapped_column(String(500), nullable=False)
    album_id: Mapped[str] = mapped_column(String(100), nullable=False)
    collection_type: Mapped[str] = mapped_column(String(20), nullable=False)
    total_tracks: Mapped[int] = mapped_column(Integer(), nullable=False)
    artist_name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='collections')
    
    






