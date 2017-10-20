import logging
from .relations import Relations
from .extrude_area_solid import ExtrudedAreaSolid
from .faceted_brep import FacetedBrep

class Representation(Relations):
    def from_json(self, json_data):
        super(Representation, self).from_json(json_data)
        self.shapes = []
        for shape_data in json_data['shapes']:
            shape = self.inst_from_type(shape_data['type'])
            shape.from_json(shape_data)
            self.shapes.append(shape)
        self.boxes = []

    def inst_from_type(self, cls_type):
        classes = {
            'ExtrudedAreaSolid': ExtrudedAreaSolid,
            'FacetedBrep': FacetedBrep
        }
        return classes[cls_type](self)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcRepresentation'), ifc_data.is_a()
        super(Representation, self).from_ifc(ifc_data)
        self.shapes = []
        self.boxes = [] # ignored for now

        ignore = [
            'IfcPolyline',
            'IfcMappedItem',
            'IfcFaceBasedSurfaceModel',
            'IfcBooleanClippingResult'
        ]
        for ifc_item in self.ifc_data.Items:
            item_type = ifc_item.is_a()
            if item_type in ignore:
                logging.info('ignore ' + item_type)
                continue
            elif item_type == 'IfcBoundingBox':
                # TODO: fill self.boxes
                # (ignored for now cause it needs to be specified in export)
                logging.info('ignore ' + item_type + ' for ' + self.parent.name)
                continue
            shape = self.inst_from_type(item_type[3:])
            shape.from_ifc(ifc_item)
            self.shapes.append(shape)

    def check_ignore(self):
        representation = self.ifc_data
        if not representation.is_a('IfcShapeRepresentation'):
            logging.info('ignoring ' + representation.is_a() +
                         ' in ' + self.parent)
            return True
        return False # do NOT ignore

    def to_json(self):
        data = super(Representation, self).to_json()
        data['boxes'] = [b.to_json() for b in self.boxes]
        data['shapes'] = [s.to_json() for s in self.shapes]
        return data

    def __init__(self, parent):
        self.parent = parent
