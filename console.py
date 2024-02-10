#!/usr/bin/python
"""The console of airbnb"""
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command-line interpreter for managing HBNB data.
    """

    prompt = "(hbnb) "
    classes = {"BaseModel", "User", "City",
               "Amenity", "State", "Place", "Review"}

    def do_EOF(self, arg):
        """
        Exit the console when EOF is reached (Ctrl + D).
        """
        return True

    def do_quit(self, arg):
        """
        Quit the console.
        """
        return True

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def help_quit(self):
        """
        Display help message for the quit command.
        """
        print("Quit command to exit the program\n")

    def do_create(self, arg):
        """
        Create a new instance of a given class.
        Usage: create <class>
        """
        args_list = shlex.split(arg)
        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{args_list[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Display the string representation of an instance.
        Usage: show <class> <id>
        """
        args_list = shlex.split(arg)
        all_instances = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args_list) < 2:
            print("** instance id missing **")
        else:
            self._show_instance(args_list, all_instances)

    def _show_instance(self, args_list, all_instances):
        """
        Display the string representation of an instance.
        """
        class_id = "{}.{}".format(args_list[0], args_list[1])
        if class_id not in all_instances:
            print("** no instance found **")
        else:
            print(all_instances[class_id])

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        args_list = shlex.split(arg)
        all_instances = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
        elif args_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args_list) < 2:
            print("** instance id missing **")
        else:
            self._destroy_instance(args_list, all_instances)

    def _destroy_instance(self, args_list, all_instances):
        """
        Delete an instance based on the class name and id.
        """
        class_id = "{}.{}".format(args_list[0], args_list[1])
        if class_id in all_instances:
            del all_instances[class_id]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Print all string representations of instances.
        Usage: all or all <class_name>
        """
        args_list = shlex.split(arg)
        all_instances = storage.all()

        if not args_list:
            print([str(value) for value in all_instances.values()])
        elif args_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            class_name = args_list[0]
            instances_by_class = [
                str(value)
                for class_id, value in all_instances.items()
                if class_id.split('.')[0] == class_name
            ]
            if instances_by_class:
                print(instances_by_class)

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        args_list = shlex.split(arg)
        all_instances = storage.all()

        if len(args_list) == 0:
            print("** class name missing **")
            return
        elif args_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args_list) < 2:
            print("** instance id missing **")
        else:
            class_id = "{}.{}".format(args_list[0], args_list[1])
            if class_id not in all_instances:
                print("** no instance found **")
            elif len(args_list) < 3:
                print("** attribute name missing **")
            elif len(args_list) < 4:
                print("** value missing **")
            else:
                self.update_instance(all_instances, class_id, args_list)

    def update_instance(self, all_instances, class_id, args_list):
        """
        Update an instance by adding or updating an attribute.
        """
        obj = all_instances[class_id]
        attr_name = args_list[2]
        attr_value = args_list[3]

        try:
            attr_value = eval(attr_value)
        except Exception:
            pass
        setattr(obj, attr_name, attr_value)

        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
