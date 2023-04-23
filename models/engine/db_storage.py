"""
    This module defines a class that is mapped to a mysql database
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.parse
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """
        This class manages the storgage in a mysql database
    """
    __engine = None
    __session = None

    def __init__(self):
        """This method initialize the DBStorage class"""

        user = os.getenv('HBNB_MYSQL_USER')
        psword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv("HBNB_ENV")
        database_url = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                user, psword, host, db_name)
        DBStorage.__engine = create_engine(database_url, pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Return a dictionary of a model object in storage"""
        obj_dict = {}
        all_models = {
                'State': State,
                'City': City,
                'User': User,
                'Place': Place,
                'Review': Review
                }

        if cls:
            query = DBStorage.__session.query(cls)
            for obj in query.all():
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
            return obj_dict

        else:
            for models, value in all_models.items():
                query = self.__session.query(value)
                for obj in query.all():
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
            return obj_dict

    def new(self, obj):
        """Add obj to the database session"""

        if obj:
            DBStorage.__session.add(obj)

    def save(self):
        """Commits the add object to the database"""
        DBStorage.__session.commit()

    def reload(self):
        """Reloads the database storage engine"""
        Base.metadata.create_all(DBStorage.__engine)
        Session = sessionmaker(bind=DBStorage.__engine, expire_on_commit=False)
        DBStorage.__session = scoped_session(Session)()

    def close(self):
        """Close database storage engine"""
        self.__session.close()


