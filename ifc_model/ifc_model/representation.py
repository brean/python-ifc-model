"""
basic representation to get mesh-id, we do not parse the representation itself.
(for now, see geometry/)
"""
from .relations import Relations


class Representation(Relations):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def from_json(self, json_data):
        super(Representation, self).from_json(json_data)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcRepresentation'), ifc_data.is_a()
        super(Representation, self).from_ifc(ifc_data)
