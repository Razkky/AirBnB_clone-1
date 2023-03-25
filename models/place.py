#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
import os
from sqlalchemy.orm import relationship


place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            nullable=False,
            primary_key=True
            ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            nullable=False,
            primary_key=True
            )
        )
class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(60), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
                'Review',
                cascade="all, delete, delete-orphan",
                backref='place'
                )
        amenities = relationship(
                'Amenity',
                secondary=place_amenity,
                viewonly=False,
                backref='place_amenities'
                )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns the review of this Place"""
            from models import storage
            place_review = []
            for key, value in storage.all(Review).items():
                if value.place_id == self.id:
                    place_review.append(value)
            return place_review

        @property
        def amenities(self):
            """Returns the amenities of this Place"""
            from models import storage
            place_amenity = []
            for key, value in storage.all(Amenity).items():
                if value.place_id in self.amenity_ids:
                    place_amenity.append(value)
            return place_amenity

        @amenities.setter
        def amenities(self, value):
            """Adds amenity id to list of amenity ids"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value)
