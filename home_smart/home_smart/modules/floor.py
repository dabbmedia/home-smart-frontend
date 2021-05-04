from .model import Model

class Floor(Model):
    def __init__(self):
        Model.__init__(self, 'floor')
        self.entity_alias = 'f'
        self.select = ('f.id', 'f.location_id', 'l.name as location', 'f.name', 'f.description', 'f.created')
        self.join = ({'join_type': 'LEFT JOIN', 'table': 'location', 'alias': 'l', 'field1': 'l.id', 'field2': 'f.location_id'},)

    def get_floors(self):
        floors = self.select_all()
        return floors

    def get_floor(self, id):
        floor = self.select_by_id(id)
        return floor