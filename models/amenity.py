#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """ Amenity Class"""
    
    __tablename__ = 'amenities'
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)

    else:
        name = ""
