

class AbstractDestinationCRUDBuilder():
    """
    Abstract class from which destination CRUD interface constructors are inherited.
    """

    def __init__(self):
        pass
        
    def build_read(self):
        """
        Build the read.
        """
        raise NotImplementedError()
        
    def build_create(self):
        """
        Build the create.
        """
        raise NotImplementedError()
    
    def build_update(self):
        """
        Builds the update.
        """
        raise NotImplementedError()
    
    def build_delete(self):
        """
        Builds the delete.
        """
        raise NotImplementedError()
    
    def build_update_or_create(self):
        """
        Build the "update or create".
        """
        raise NotImplementedError()