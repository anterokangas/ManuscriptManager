def get_all_subclasses(cls, include_itself=False):
    """" Recursively find all subclasses of a given class cls

    Parameters
    ----------
    cls :   the beginning class
    include_itself : if True the the class itself is included

    Returns
    -------
    tuple of class names
    """
    all_subclasses = [cls] if include_itself else []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return tuple(all_subclasses)
