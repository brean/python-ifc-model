from ifc_model.relations import Relations


class CircleProfileDef(Relations):
    def __init__(self, representation):
        self.representation = representation
        self.type = 'CircleProfileDef'

    def to_json(self):
        data = super(CircleProfileDef, self).to_json()
        data['type'] = self.type
        return data
