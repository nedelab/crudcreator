class EntityAlreadyExist(Exception):
    """
    Raised if an entity tries to be created while another entity, with the same ids, already exists.
    """
    pass

class EntityNotExist(Exception):
    """
    Raised if you try to perform an action (delete, update, etc.) on an entity that does not exist.
    """
    pass