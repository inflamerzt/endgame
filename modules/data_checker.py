from modules.type_checker import *


def check(data):
    if isinstance(data, list):
        if is_list_of_scalar(data):
            return "los"
        elif is_list_of_scalar_dict(data):
            return "losd"
        else:
            return "tree"
    elif isinstance(data, dict):
        # Check values whether they are scalars
        if all(isinstance(value, dict) for value in data.values()):
            if all(
                    is_list_of_scalar(value.values())
                    for value in data.values()):
                print("dosd1")
                return "dosd"
            else:
                return "tree"
        else:
            if is_list_of_scalar(data.values()):
                return "sd"
            elif all(is_list_of_scalar(value) for value in data.values()):
                return "sd"
            else:
                return "tree"
    else:
        return "tree"
