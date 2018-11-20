from ifc_model.relations import Relations


class RectangleProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'RectangleProfileDef'

    def to_json(self):
        data = super(RectangleProfileDef, self).to_json()
        data['type'] = self.type
        return data
