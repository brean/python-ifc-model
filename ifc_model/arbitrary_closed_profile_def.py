from .relations import Relations
from .point import Point

class ArbitraryClosedProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ArbitraryClosedProfileDef'

    def to_json(self):
        data = super(ArbitraryClosedProfileDef, self).to_json()
        data['type'] = self.type
        data['points'] = [p.to_json() for p in self.points]
        return data

    def from_json(self, data):
        super(ArbitraryClosedProfileDef, self).from_json(data)
        self.type = data['type']
        self.points = self.cls_from_json(Point, data['points'])

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcArbitraryClosedProfileDef')
        # print(json.dumps(debug(ifc_data), indent=2))
        if ifc_data.OuterCurve.is_a('IfcCompositeCurve'):
            #TODO: Curves
            self.points = []
        else:
            self.points = self.cls_from_ifc(Point, ifc_data.OuterCurve.Points)
        super(ArbitraryClosedProfileDef, self).from_ifc(ifc_data)
