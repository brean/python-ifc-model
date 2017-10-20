from .relations import Relations
from .point import Point

'''
segment either an IfcPolyline or an IfcTrimmedCurve
'''
class Segment(Relations):
    def from_json(self, data):
        super(Segment, self).from_json(data)
        self.type = data['type']
        if self.type == 'Polyline':
            self.points = self.cls_from_json(Point, data['points'])
        elif self.type == 'TrimmedCurve':
            self.center = Point(self)
            self.center.from_json(data['center'])
            self.radius = data['radius']


    def to_json(self):
        data = super(Segment, self).to_json()
        data['type'] = self.type
        if self.type == 'Polyline':
            data['points'] = [p.to_json() for p in self.points]
        elif self.type == 'TrimmedCurve':
            data['center'] = self.center.to_json()
            data['radius'] = self.radius
        return data

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcCompositeCurveSegment')
        super(Segment, self).from_ifc(ifc_data)
        ifc_curve = ifc_data.ParentCurve
        self.type = ifc_curve.is_a()[3:]
        if self.type == 'Polyline':
            self.points = self.cls_from_ifc(Point, ifc_data.ParentCurve.Points)
        elif self.type == 'TrimmedCurve':
            # TODO: this is just start and end point - direct line, no curve
            self.center = Point(self)
            self.center.from_ifc(ifc_curve.BasisCurve.Position.Location)
            self.radius = ifc_curve.BasisCurve.Radius
        else:
            raise Exception(ifc_curve.is_a(), ifc_curve.id())

    def __init__(self, parent):
        self.parent = parent
