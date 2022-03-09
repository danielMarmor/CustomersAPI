class NotFoundException(Exception):
    def __init__(self, message, entity, entity_id):
        super().__init__(message)
        self.entity = entity
        self.entity_id = entity_id

