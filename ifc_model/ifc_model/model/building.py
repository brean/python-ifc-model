class Building(object):
    def __init__(self, site, name, global_id=None, description=None,
                 long_name=None, elevation_of_ref_height=None,
                 elevation_of_terrain=None, address=None):
        self.site = site
        site.buildings.append(self)
        self.global_id = global_id
        self.name = name
        self.long_name = long_name
        self.description = description
        self.elevation_of_terrain = elevation_of_terrain
        self.elevation_of_ref_height = elevation_of_ref_height
        self.address = address
        self.storeys = []
        self.products = []

    def to_dict(self):
        data = self.__dict__
        data['address'] = self.address.__dict__ if self.address else None
        data['storeys'] = [s.to_dict() for s in self.storeys]
        data['products'] = [p.to_dict() for p in self.products]
        del data['site']
        return data
