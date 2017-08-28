from .relations import Relations
from .point import Point
from .segment import Segment

class ArbitraryClosedProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ArbitraryClosedProfileDef'
        self.points = None
        self.segments = None

    def to_json(self):
        data = super(ArbitraryClosedProfileDef, self).to_json()
        data['type'] = self.type
        if self.points:
            data['points'] = [p.to_json() for p in self.points]
        if self.segments:
            data['segments'] = [s.to_json() for s in self.segments]
        data['outer_curve_type'] = self.outer_curve_type
        return data

    def from_json(self, data):
        super(ArbitraryClosedProfileDef, self).from_json(data)
        self.type = data['type']
        self.outer_curve_type = data['outer_curve_type']
        if 'points' in data:
            self.points = self.cls_from_json(Point, data['points'])
        if 'segments' in data:
            self.segments = self.cls_from_json(Segment, data['segments'])

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcArbitraryClosedProfileDef')
        # print(json.dumps(debug(ifc_data), indent=2))
        self.outer_curve_type = ifc_data.OuterCurve.is_a()[3:]
        if ifc_data.OuterCurve.is_a('IfcCompositeCurve'):
            self.segments = self.cls_from_ifc(Segment, ifc_data.OuterCurve.Segments)
        else:
            # just connects the points
            self.points = self.cls_from_ifc(Point, ifc_data.OuterCurve.Points)
        super(ArbitraryClosedProfileDef, self).from_ifc(ifc_data)
