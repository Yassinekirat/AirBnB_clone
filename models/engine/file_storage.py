#!/usr/bin/python3
"""
Module for serializing and deserializing data
"""
import json
import os
from pathlib import Path
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    FileStorage class for storing, serializing and deserializing data
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Retrieve all objects stored."""
        all_objects = FileStorage.__objects
        return all_objects

    def new(self, obj):
        """Add a new object to the storage."""
        class_name = obj.__class__.__name__
        object_key = f"{class_name}.{obj.id}"
        FileStorage.__objects[object_key] = obj

    def save(self):
        """Save the objects to the JSON file."""
        all_objects = FileStorage.__objects
        obj_dict = {
            obj_key: all_objects[obj_key].to_dict()
            for obj_key in all_objects
        }

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Reload objects from the JSON file."""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as file:
                try:
                    self.__load_objects_from_json(file)
                except Exception:
                    pass

    def __load_objects_from_json(self, file):
        """Load objects from a JSON file."""
        obj_dict = json.load(file)
        for key, value in obj_dict.items():
            class_name, obj_id = key.split('.')
            self.__objects[key] = eval(class_name)(**value)
