#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DATETIME, nullable=False, default=datetime.utcnow())
    updated_at = Column(DATETIME, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            if not hasattr(kwargs, 'id'):
                setattr(self, 'id', str(uuid.uuid4()))
            if not hasattr(kwargs, 'created_at'):
                setattr(self, 'created_at', datetime.now())
            if not hasattr(kwargs, 'updated_at'):
                setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        new_dict = {}
        new_dict.update(self.__dict__)
        del new_dict['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, new_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    dictionary[key] = value.isoformat()
                else:
                    dictionary[key] = value
        dictionary['__class__'] = self.__class__.__name__

        return dictionary
