import logging
from .relations import Relations
# basic representation to get mesh-id, we do not parse the representation itself.
# (for now, see geometry/)

class Representation(Relations):
    def __init__(self, parent):
        self.parent = parent

    def from_json(self, json_data):
        super(Representation, self).from_json(json_data)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcRepresentation'), ifc_data.is_a()
        super(Representation, self).from_ifc(ifc_data)
