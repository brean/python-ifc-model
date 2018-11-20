from .representation_item import RepresentationItem
from .arbitrary_closed_profile_def import ArbitraryClosedProfileDef
from .arbitrary_profile_def_with_voids import ArbitraryProfileDefWithVoids
from .rectangle_profile_def import RectangleProfileDef
from .i_shape_profile_def import IShapeProfileDef
from .circle_profile_def import CircleProfileDef

"""
see also faceted_brep
"""


class ExtrudedAreaSolid(RepresentationItem):
    def __init__(self, representation):
        self.representation = representation
        self.type = 'ExtrudedAreaSolid'
        self.location = None
        self.direction = None
        self.axis = None
        self.depth = None
        self.area = None

    def area_from_class(self, name):
        classes = {
            'ArbitraryClosedProfileDef': ArbitraryClosedProfileDef,
            'ArbitraryProfileDefWithVoids': ArbitraryProfileDefWithVoids,
            'RectangleProfileDef': RectangleProfileDef,
            'IShapeProfileDef': IShapeProfileDef,
            'CircleProfileDef': CircleProfileDef
        }
        return classes[name](self)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcExtrudedAreaSolid')
        super(ExtrudedAreaSolid, self).from_ifc(ifc_data)
        # TODO: ifc_data.Position is a Axis2Placement3D, maybe get an own class?
        self.location = ifc_data.Position.Location.Coordinates
        self.direction = None
        if ifc_data.Position.RefDirection:
            self.direction = ifc_data.Position.RefDirection.DirectionRatios
        self.axis = None
        if self.ifc_data.Position.Axis:
            self.axis = self.ifc_data.Position.Axis.DirectionRatios
        area_type = self.ifc_data.SweptArea.is_a()
        self.depth = self.ifc_data.Depth
        self.area = self.area_from_class(area_type[3:])
        self.area.from_ifc(self.ifc_data.SweptArea)

    def from_json(self, data):
        super(ExtrudedAreaSolid, self).from_json(data)
        self.area = self.area_from_class(data['area']['type'])
        self.depth = data['depth']
        self.axis = data['axis']
        self.location = data['location']
        self.direction = data['direction']
        self.area.from_json(data['area'])

    def to_json(self):
        data = super(ExtrudedAreaSolid, self).to_json()
        data['type'] = self.type
        data['depth'] = self.depth
        data['location'] = self.location
        data['axis'] = self.axis
        data['direction'] = self.direction
        data['area'] = self.area.to_json()
        return data
