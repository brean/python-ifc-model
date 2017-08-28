from .relations import Relations

class RepresentationItem(Relations):
    def to_json(self):
        data = super(RepresentationItem, self).to_json()
        data['type'] = self.type
        data['location'] = self.location
        return data

    def from_json(self, data):
        super(RepresentationItem, self).from_json(data)
        self.location = data['location']
