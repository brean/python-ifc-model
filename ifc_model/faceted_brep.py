from .representation_item import RepresentationItem

class FacetedBrep(RepresentationItem):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'FacetedBrep'

    def to_json(self):
        data = super(FacetedBrep, self).to_json()
        return data

    def from_json(self, data):
        super(FacetedBrep, self).from_json(data)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcFacetedBrep')
        super(FacetedBrep, self).from_ifc(ifc_data)
        self.location = (0, 0, 0)
        self.outer_faces = []
        # TODO: Face
        #for face in ifc_data.Outer.CfsFaces:
        #    self.faces.append()
