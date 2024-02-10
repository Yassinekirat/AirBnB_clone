#!/usr/bin/python3
"BaseModel class"

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    Base class for all models.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize a BaseModel instance.
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if kwargs:
            self.process_kwargs(kwargs)
        models.storage.new(self)

    def process_kwargs(self, kwargs):
        """
        Process keyword arguments and set instance attributes accordingly.
        """
        for key, value in kwargs.items():
            time_format = "%Y-%m-%dT%H:%M:%S.%f"
            if key == "__class__":
                continue
            elif key in ("created_at", "updated_at"):
                setattr(self, key, datetime.strptime(value, time_format))
            else:
                setattr(self, key, value)

    def __str__(self):
        """
        Return a string representation of the BaseModel instance.
        """
        cls_name = self.__class__.__name__
        return f"[{cls_name}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Save the BaseModel instance and update the 'updated_at' attribute.
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Return a dictionary representation of the BaseModel instance.
        """
        new_dictionary = self.__dict__.copy()
        new_dictionary["__class__"] = self.__class__.__name__
        new_dictionary["created_at"] = self.created_at.isoformat()
        new_dictionary["updated_at"] = self.updated_at.isoformat()

        return new_dictionary
