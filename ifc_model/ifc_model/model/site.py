class Site(object):
    def __init__(self, project, name, global_id=None, description=None,
                 long_name=None, address=None,
                 buildings=None, representations=None,
                 latitude=None, longitude=None, elevation=0.0):
        self.project = project
        project.sites.append(self)
        self.global_id = global_id
        self.description = description
        self.name = name
        self.long_name = long_name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.address = address
        self.buildings = buildings if buildings else []
        self.representations = representations if representations else []

    def to_dict(self):
        data = self.__dict__
        data['address'] = self.address.__dict__ if self.address else None
        data['buildings'] = [b.to_dict() for b in self.buildings]
        del data['project']
        return data


class Address(object):
    def __init__(self, internal_location=None, address_lines=None,
                 postal_box=None, town=None, region=None, postal_code=None,
                 country=None):
        self.internal_location = internal_location
        self.address_lines = address_lines if address_lines else []
        self.postal_box = postal_box
        self.town = town
        self.region = region
        self.postal_code = postal_code
        self.country = country
