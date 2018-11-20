from ifc_model.relations import Relations

'''
see faceted_brep and extrude_area_solid
'''


class RepresentationItem(Relations):
    def __init__(self):
        self.type = None
        self.location = (0, 0, 0)

    def to_json(self):
        data = super(RepresentationItem, self).to_json()
        data['type'] = self.type
        data['location'] = self.location
        return data

    def from_json(self, data):
        super(RepresentationItem, self).from_json(data)
        self.location = data['location']
