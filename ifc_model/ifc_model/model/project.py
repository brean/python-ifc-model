import time

"""
the main project

The structure is:
  project (including meta information)
    site
      building
        storey
          space
            product
          product
        product
        
a product has a location as wall as a representation
"""


class Project(object):
    def __init__(self, filename, global_id=None, name='', long_name='',
                 description=None, created=None,
                 creator=None, organization=None):
        """
        main project

        Parameters
        ----------
        filename : str
            full path of the ifc file (including ending)
        global_id : str
            generated id, will be created by the exporter if not set
        name : str
            name of the project
        long_name : str
            detailed name of the project
        description : str
            description of the project
        created : time.time()
            timestamp when the project has been created (in seconds)
        creator : str
            name of the person who created the IFC-file (e.g. 'John Doe')
        organization : str
            name of the organization the creator belongs to (e.g. 'ACME Corp.')
        """
        self.global_id = global_id
        self.long_name = long_name
        self.name = name
        self.description = description
        self.created = created if created else time.time()
        self.organization = organization
        self.creator = creator
        self.filename = filename
        self.sites = []

    def to_dict(self):
        data = self.__dict__
        data['sites'] = [s.to_dict() for s in self.sites]
        return data
