from .relations import Relations
#from .representation import Representation

class Product(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcProduct')
        super(Product, self).from_ifc(ifc_data)
        self.name = ifc_data.Name
        ifc_type = self.ifc_data.is_a()
        assert ifc_type.startswith('Ifc')
        self.ifc_type = ifc_type[3:].lower()

        #self.representations = []
        #if self.ifc_data.Representation:
        #    self.representations = self.cls_from_ifc(
        #        Representation,
        #        self.ifc_data.Representation.Representations
        #    )


    def from_json(self, data):
        super(Product, self).from_json(data)
        self.name = data['name']
        self.ifc_type = data['type']
        #self.representations = self.cls_from_json(Representation, data['representations'])

    def to_json(self):
        data = super(Product, self).to_json()
        data['name'] = self.name
        data['type'] = self.ifc_type
        #data['representations'] = [r.to_json() for r in self.representations]
        return data

    def __init__(self, parent):
        self.parent = parent
