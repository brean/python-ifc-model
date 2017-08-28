from .relations import Relations

class Point(Relations):
    def from_json(self, data):
        super(Point, self).from_json(data)
        self.coords = data['coords']
        self.type = data['type']

    def to_json(self):
        data = super(Point, self).to_json()
        data['coords'] = self.coords
        data['type'] = self.type
        return data

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcCartesianPoint')
        super(Point, self).from_ifc(ifc_data)
        self.type = ifc_data.is_a()[3:]
        self.coords = ifc_data.Coordinates

    def __init__(self, parent):
        self.parent = parent
