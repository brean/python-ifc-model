class Storey(object):
    def __init__(self, building, name, global_id=None, long_name=None,
                 description=None, elevation=0.0):
        self.building = building
        building.storeys.append(self)
        self.name = name
        self.global_id = global_id
        self.description = description
        self.long_name = long_name
        self.elevation = elevation
        self.spaces = []
        self.products = []

    def to_dict(self):
        data = self.__dict__
        data['spaces'] = [s.to_dict() for s in self.spaces]
        data['products'] = [p.to_dict() for p in self.products]
        del data['building']
        return data