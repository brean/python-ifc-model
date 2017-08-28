#!/bin/python
# -*- coding: UTF-8 -*-
# Ifc-Model based on the ifc openshell
import os
import logging
import json

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

    def get_representations_from_ifc(self):
        self.representations = []
        if self.ifc_data.Representation:
            self.representations = self.cls_from_ifc(
                Representation,
                self.ifc_data.Representation.Representations
            )


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


class Product(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcProduct')
        super(Product, self).from_ifc(ifc_data)
        self.name = ifc_data.Name
        ifc_type = self.ifc_data.is_a()
        assert ifc_type.startswith('Ifc')
        self.ifc_type = ifc_type[3:].lower()
        self.representations = []
        # TODO representation for product
        #self.get_representations_from_ifc()


    def from_json(self, data):
        super(Product, self).from_json(data)
        self.name = data['name']
        self.ifc_type = data['type']
        self.representations = self.cls_from_json(Representation, data['representations'])

    def to_json(self):
        data = super(Product, self).to_json()
        data['name'] = self.name
        data['type'] = self.ifc_type
        data['representations'] = [r.to_json() for r in self.representations]
        return data

    def __init__(self, parent):
        self.parent = parent


class Space(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcSpace')
        super(Space, self).from_ifc(ifc_data)
        self.name = ifc_data.Name
        self.get_representations_from_ifc()
        self.products = self.cls_from_ifc(
            Product,
            self.get_related_elements(ifc_data)
        )


    def from_json(self, data):
        super(Space, self).from_json(data)
        self.name = data['name']
        self.products = self.cls_from_json(Product, data['products'])
        self.representations = self.cls_from_json(Representation, data['representations'])

    def to_json(self):
        data = super(Space, self).to_json()
        data['name'] = self.name
        data['products'] = [p.to_json() for p in self.products]
        data['representations'] = [r.to_json() for r in self.representations]
        return data

    def __init__(self, storey):
        self.storey = storey

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
        self.get_representations_from_ifc()

    def from_json(self, data):
        super(Storey, self).from_json(data)
        self.name = data['name']
        self.long_name = data['long_name']
        self.elevation = data['elevation']
        self.spaces = self.cls_from_json(Space, data['spaces'])
        self.products = self.cls_from_json(Product, data['products'])
        self.representations = self.cls_from_json(Representation, data['representations'])

    def to_json(self):
        data = super(Storey, self).to_json()
        data['name'] = self.name
        data['long_name'] = self.long_name
        data['elevation'] = self.elevation
        data['spaces'] = [s.to_json() for s in self.spaces]
        data['products'] = [p.to_json() for p in self.products]
        data['representations'] = [r.to_json() for r in self.representations]
        return data

    def __init__(self, building):
        self.building = building


class Building(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcBuilding')
        super(Building, self).from_ifc(ifc_data)
        self.name = ifc_data.Name
        self.storeys = self.cls_from_ifc(
            Storey,
            self.get_related_objects(ifc_data)
        )

    def from_json(self, data):
        super(Building, self).from_json(data)
        self.name = data['name']
        self.storeys = self.cls_from_json(Storey, data['storeys'])

    def to_json(self):
        data = super(Building, self).to_json()
        data['name'] = self.name
        data['storeys'] = [s.to_json() for s in self.storeys]
        return data

    def __init__(self, site):
        self.site = site


class RepresentationItem(Relations):
    def to_json(self):
        data = super(RepresentationItem, self).to_json()
        data['type'] = self.type
        data['location'] = self.location
        return data

    def from_json(self, data):
        super(RepresentationItem, self).from_json(data)
        self.location = data['location']

class Face(Relations):
    # TODO Bounds[0].Bound.Polygon[i].Coordinates (only Faceted Brep)
    pass

class FacetedBrep(RepresentationItem):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'FacetedBrep'

    def to_json(self):
        data = super(FacetedBrep, self).to_json()
        return data

    def from_json(self, data):
        super(FacetedBrep, self).from_json(data)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcFacetedBrep')
        super(FacetedBrep, self).from_ifc(ifc_data)
        self.location = (0, 0, 0)
        self.outer_faces = []
        # TODO: Face
        #for face in ifc_data.Outer.CfsFaces:
        #    self.faces.append()

class Point(Relations):
    def from_json(self, data):
        super(Point, self).from_json(data)
        self.coords = data['coords']
        self.type = data['type']

    def to_json(self):
        data = super(Point, self).to_json()
        data['coords'] = self.coords
        data['type'] = self.type
        return data

    def from_ifc(self, ifc_data):
        super(Point, self).from_ifc(ifc_data)
        self.type = ifc_data.is_a()[3:]
        self.coords = ifc_data.Coordinates

    def __init__(self, parent):
        self.parent = parent


class ArbitraryClosedProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ArbitraryClosedProfileDef'

    def to_json(self):
        data = super(ArbitraryClosedProfileDef, self).to_json()
        data['type'] = self.type
        data['points'] = [p.to_json() for p in self.points]
        return data

    def from_json(self, data):
        super(ArbitraryClosedProfileDef, self).from_json(data)
        self.type = data['type']
        self.points = self.cls_from_json(Point, data['points'])

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcArbitraryClosedProfileDef')
        # print(json.dumps(debug(ifc_data), indent=2))
        if ifc_data.OuterCurve.is_a('IfcCompositeCurve'):
            #TODO: Curves
            self.points = []
        else:
            self.points = self.cls_from_ifc(Point, ifc_data.OuterCurve.Points)
        super(ArbitraryClosedProfileDef, self).from_ifc(ifc_data)

class ArbitraryProfileDefWithVoids(ArbitraryClosedProfileDef):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ArbitraryProfileDefWithVoids'

class RectangleProfileDef(Relations):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'RectangleProfileDef'

    def to_json(self):
        data = super(RectangleProfileDef, self).to_json()
        data['type'] = self.type
        return data

class ExtrudedAreaSolid(RepresentationItem):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ExtrudedAreaSolid'

    def area_from_class(self, name):
        classes = {
            'ArbitraryClosedProfileDef': ArbitraryClosedProfileDef,
            'ArbitraryProfileDefWithVoids': ArbitraryProfileDefWithVoids,
            'RectangleProfileDef': RectangleProfileDef
        }
        return classes[name](self)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcExtrudedAreaSolid')
        super(ExtrudedAreaSolid, self).from_ifc(ifc_data)
        self.location = ifc_data.Position.Location.Coordinates
        area_type = self.ifc_data.SweptArea.is_a()
        self.area = self.area_from_class(area_type[3:])
        self.area.from_ifc(self.ifc_data.SweptArea)

    def from_json(self, data):
        super(ExtrudedAreaSolid, self).from_json(data)
        self.area = self.area_from_class(data['area']['type'])
        self.area.from_json(data['area'])

    def to_json(self):
        data = super(ExtrudedAreaSolid, self).to_json()
        data['type'] = self.type
        data['area'] = self.area.to_json()
        return data


class Representation(Relations):
    def from_json(self, json_data):
        super(Representation, self).from_json(json_data)
        self.shapes = []
        for shape_data in json_data['shapes']:
            shape = self.inst_from_type(shape_data['type'])
            shape.from_json(shape_data)
            self.shapes.append(shape)
        self.boxes = []

    def inst_from_type(self, cls_type):
        classes = {
            'ExtrudedAreaSolid': ExtrudedAreaSolid,
            'FacetedBrep': FacetedBrep
        }
        return classes[cls_type](self)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcRepresentation'), ifc_data.is_a()
        super(Representation, self).from_ifc(ifc_data)
        self.shapes = []
        self.boxes = [] # ignored for now

        ignore = [
            'IfcPolyline',
            'IfcMappedItem',
            'IfcFaceBasedSurfaceModel',
            'IfcBooleanClippingResult'
        ]
        for ifc_item in self.ifc_data.Items:
            item_type = ifc_item.is_a()
            if item_type in ignore:
                logging.info('ignore ' + item_type)
                continue
            elif item_type == 'IfcBoundingBox':
                # TODO: fill self.boxes
                # (ignored for now cause it needs to be specified in export)
                logging.info('ignore ' + item_type + ' for ' + self.parent.name)
                continue
            shape = self.inst_from_type(item_type[3:])
            shape.from_ifc(ifc_item)
            self.shapes.append(shape)

    def check_ignore(self):
        representation = self.ifc_data
        if not representation.is_a('IfcShapeRepresentation'):
            logging.info('ignoring ' + representation.is_a() +
                         ' in ' + self.parent)
            return True
        return False # do NOT ignore

    def to_json(self):
        data = super(Representation, self).to_json()
        data['boxes'] = [b.to_json() for b in self.boxes]
        data['shapes'] = [s.to_json() for s in self.shapes]
        return data

    def __init__(self, parent):
        self.parent = parent


class Site(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcSite')
        super(Site, self).from_ifc(ifc_data)

        self.global_id = ifc_data.GlobalId
        self.name = ifc_data.Name

        ifc_project = self.project.ifc_data
        assert ifc_project
        if ifc_data.Decomposes:
            assert len(ifc_data.Decomposes) == 1, \
                'Only one IfcProject per IFC file ' \
                '(only one per IfcSite) is allowed'
            ifc_decomposes = ifc_data.Decomposes[0]
            assert ifc_decomposes.id() == ifc_project.id(), \
                'mismatching project id for this site.'
        else:
            # TODO: bug report to Autodesk?
            logging.warn('IfcSite is not connected to the IfcProject. ' \
                         'We assume there is only one connection, this is ' \
                         'not conform with the the IFC specification')
        self.buildings = self.cls_from_ifc(
            Building,
            self.get_related_objects(ifc_data)
        )

        self.get_representations_from_ifc()

    def from_json(self, data):
        super(Site, self).from_json(data)
        self.global_id = data['global_id']
        self.name = data['name']
        self.buildings = self.cls_from_json(Building, data['buildings'])
        self.representations = self.cls_from_json(Representation, data['representations'])

    def to_json(self):
        data = super(Site, self).to_json()
        data['global_id'] = self.global_id
        data['name'] = self.name
        data['buildings'] = [b.to_json() for b in self.buildings]
        data['representations'] = [r.to_json() for r in self.representations]
        return data

    def __init__(self, project):
        self.project = project

class Project(Relations):
    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcProject')
        super(Project, self).from_ifc(ifc_data)
        # immutable types
        self.global_id = ifc_data.GlobalId
        self.long_name = ifc_data.LongName
        self.name = ifc_data.Name
        # parse more complex data structures
        self.sites = self.cls_from_ifc(Site, self.ifc_file.by_type('ifcsite'))

    def from_json(self, data):
        super(Project, self).from_json(data)
        self.global_id = data['global_id']
        self.long_name = data['long_name']
        self.name = data['name']
        self.sites = self.cls_from_json(Site, data['sites'])

    def to_json(self):
        data = super(Project, self).to_json()
        data['global_id'] = self.global_id
        data['long_name'] = self.long_name
        data['name'] = self.name
        data['sites'] = [site.to_json() for site in self.sites]
        return data

    def open_ifc(self, filename):
        import ifcopenshell
        self.filename, ext = os.path.splitext(filename)
        assert ext == '.ifc'
        self.ifc_file = ifcopenshell.open(filename)
        ifc_projects = self.ifc_file.by_type('ifcproject')
        # only one project is allows per ifc file!
        assert len(ifc_projects) == 1, 'Only one IfcProject per Ifc-file is allowed'
        ifc_project = ifc_projects[0]
        self.ifc_data = ifc_project
        self.from_ifc(ifc_project)

    def save_json(self):
        filename = self.filename + '.json'
        json.dump(self.to_json(), open(filename, 'w'), indent=2, sort_keys=True)
        return filename
