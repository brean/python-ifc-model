'''
helper functions to resolve ifc relations
'''
class Relations(object):
    '''
    get relating objects from IfcRelDecomposes -> IfcRelAggregates
    see /ifckernel/lexical/ifcreldecomposes.htm
    '''
    def get_related_objects(self, obj, is_a='IfcRelAggregates'):
        related_objects = []
        # IsDecomposedBy is a set of IfcRelDecomposes
        # (IfcRelAggregates or IfcRelNests)
        for decomp in obj.IsDecomposedBy:
            if not decomp.is_a(is_a):
                logging.warn('No {} according to standard!'.format(is_a))
            # IfcRelNets and IfcRelAggregates require to have at least 1
            # element is set!
            # see /ifckernel/lexical/ifcrelnests.htm
            # and /ifckernel/lexical/ifcrelaggregates.htm
            assert len(decomp.RelatedObjects) >= 1
            # list of IfcObjectDefinition, e.g. storey, space or building
            related_objects += decomp.RelatedObjects
        return related_objects

    '''
    get containing objects from IfcRelContainedInSpatialStructure -> IfcProduct
    see /ifcproductextension/lexical/ifcrelcontainedinspatialstructure.htm
    '''
    def get_related_elements(self, obj, is_a='IfcRelContainedInSpatialStructure'):
        elements = []
        # ContainsElements is an IfcRelContainedInSpatialStructure
        # (IfcSpace and IfcStorey)
        for elem in obj.ContainsElements:
            if is_a:
                assert elem.is_a(is_a)
            # RelatedElements required to have at least 1 element set!
            # see /ifcproductextension/lexical/ifcrelcontainedinspatialstructure.htm
            assert len(elem.RelatedElements) >= 1
            # list of IfcProduct
            elements += elem.RelatedElements
        return elements

    def to_json(self):
        data = {'id': self.id}
        return data

    def from_ifc(self, ifc_data):
        self.ifc_data = ifc_data
        self.id = ifc_data.id()

    def cls_from_ifc(self, cls, ifc_list):
        data = []
        for ifc_data in ifc_list:
            inst = cls(self)
            data.append(inst)
            inst.from_ifc(ifc_data)
        return data

    def cls_from_json(self, cls, json_list):
        data = []
        for json_data in json_list:
            inst = cls(self)
            data.append(inst)
            inst.from_json(json_data)
        return data

    def from_json(self, data):
        self.id = data['id']
