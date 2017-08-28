import os
import json
from .relations import Relations
from .site import Site

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
