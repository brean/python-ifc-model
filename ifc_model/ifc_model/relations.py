"""
helper functions to resolve ifc relations
"""
import logging


def get_related_objects(obj, is_a='IfcRelAggregates'):
    """
    get relating objects from IfcRelDecomposes -> IfcRelAggregates
    see /ifckernel/lexical/ifcreldecomposes.htm
    """
    related_objects = []
    # IsDecomposedBy is a set of IfcRelDecomposes
    # (IfcRelAggregates or IfcRelNests)
    for decomp in obj.IsDecomposedBy:
        if not decomp.is_a(is_a):
            logging.warning('No {} according to standard!'.format(is_a))
        # IfcRelNets and IfcRelAggregates require to have at least 1
        # element is set!
        # see /ifckernel/lexical/ifcrelnests.htm
        # and /ifckernel/lexical/ifcrelaggregates.htm
        assert len(decomp.RelatedObjects) >= 1
        # list of IfcObjectDefinition, e.g. storey, space or building
        related_objects += decomp.RelatedObjects
    return related_objects


def get_related_elements(obj, is_a='IfcRelContainedInSpatialStructure'):
    """
    get containing objects from IfcRelContainedInSpatialStructure -> IfcProduct
    see /ifcproductextension/lexical/ifcrelcontainedinspatialstructure.htm
    """
    elements = []
    # ContainsElements is an IfcRelContainedInSpatialStructure
    # (IfcSpace and IfcStorey)
    for elem in obj.ContainsElements:
        if is_a:
            assert elem.is_a(is_a)
        # RelatedElements required to have at least 1 element set!
        # see
        # /ifcproductextension/lexical/ifcrelcontainedinspatialstructure.htm
        assert len(elem.RelatedElements) >= 1
        # list of IfcProduct
        elements += elem.RelatedElements
    return elements
