import logging
from .relations import Relations
from .building import Building
from .representation import Representation

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

        self.representations = []
        if self.ifc_data.Representation:
            self.representations = self.cls_from_ifc(
                Representation,
                self.ifc_data.Representation.Representations
            )

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
