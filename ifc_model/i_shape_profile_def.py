from .relations import Relations

class IShapeProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'IShapeProfileDef'

    def to_json(self):
        data = super(IShapeProfileDef, self).to_json()
        data['type'] = self.type
        return data
