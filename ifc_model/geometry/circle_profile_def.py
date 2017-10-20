from .relations import Relations

class CircleProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'CircleProfileDef'

    def to_json(self):
        data = super(CircleProfileDef, self).to_json()
        data['type'] = self.type
        return data
