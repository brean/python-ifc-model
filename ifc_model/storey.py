from .relations import Relations
from .product import Product
from .space import Space
#from .representation import Representation

'''
spaces/rooms and products,
see /ifcproductextension/lexical/ifcbuildingstorey.htm
'''
class Storey(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcBuildingStorey')
        super(Storey, self).from_ifc(ifc_data)
        self.spaces = self.cls_from_ifc(
            Space,
            self.get_related_objects(ifc_data)
        )
        self.name = ifc_data.Name
        self.long_name = ifc_data.LongName
        self.products = self.cls_from_ifc(
            Product,
            self.get_related_elements(ifc_data)
        )
        self.elevation = ifc_data.Elevation
        #self.representations = []
        #if self.ifc_data.Representation:
        #    self.representations = self.cls_from_ifc(
        #        Representation,
        #        self.ifc_data.Representation.Representations
        #    )

    def from_json(self, data):
        super(Storey, self).from_json(data)
        self.name = data['name']
        self.long_name = data['long_name']
        self.elevation = data['elevation']
        self.spaces = self.cls_from_json(Space, data['spaces'])
        self.products = self.cls_from_json(Product, data['products'])
        #self.representations = self.cls_from_json(Representation, data['representations'])

    def to_json(self):
        data = super(Storey, self).to_json()
        data['name'] = self.name
        data['long_name'] = self.long_name
        data['elevation'] = self.elevation
        data['spaces'] = [s.to_json() for s in self.spaces]
        data['products'] = [p.to_json() for p in self.products]
        #data['representations'] = [r.to_json() for r in self.representations]
        return data

    def __init__(self, building):
        self.building = building
