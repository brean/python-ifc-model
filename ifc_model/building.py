from .relations import Relations
from .storey import Storey

class Building(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcBuilding')
        super(Building, self).from_ifc(ifc_data)
        self.name = ifc_data.Name
        self.storeys = self.cls_from_ifc(
            Storey,
            self.get_related_objects(ifc_data)
        )

    def from_json(self, data):
        super(Building, self).from_json(data)
        self.name = data['name']
        self.storeys = self.cls_from_json(Storey, data['storeys'])

    def to_json(self):
        data = super(Building, self).to_json()
        data['name'] = self.name
        data['storeys'] = [s.to_json() for s in self.storeys]
        return data

    def __init__(self, site):
        self.site = site
