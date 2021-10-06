def is_scalar(value):
    return isinstance(value, (int, float, str, bool, type(None)))


def is_list_of_scalar(lst):
    if is_scalar(lst):
        return False
    else:
        return all(is_scalar(e) for e in lst)


def is_list_of_dict(lst):
    return all(isinstance(e) for e in lst)


def is_list_of_scalar_dict(lst):
    return all(isinstance(e, dict) and is_list_of_scalar(e.values()) for e in lst)
