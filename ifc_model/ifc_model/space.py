from .relations import Relations
from .product import Product
from .representation import Representation


class Space(Relations):
    def __init__(self, storey):
        super().__init__()
        self.storey = storey
        self.name = ''
        self.representations = []
        self.products = []

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcSpace')
        super(Space, self).from_ifc(ifc_data)
        self.name = ifc_data.Name
        self.representations = []
        if self.ifc_data.Representation:
            self.representations = self.cls_from_ifc(
                Representation,
                self.ifc_data.Representation.Representations
            )
        self.products = self.cls_from_ifc(
            Product,
            Relations.get_related_elements(ifc_data)
        )

    def from_json(self, data):
        super(Space, self).from_json(data)
        self.name = data['name']
        self.products = self.cls_from_json(Product, data['products'])
        self.representations = self.cls_from_json(
            Representation, data['representations'])

    def to_json(self):
        data = super(Space, self).to_json()
        data['name'] = self.name
        data['products'] = [p.to_json() for p in self.products]
        data['representations'] = [r.to_json() for r in self.representations]
        return data
