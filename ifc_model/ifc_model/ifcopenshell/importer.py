import ifcopenshell
from ifc_model.relations import get_related_objects, get_related_elements
from ifc_model.model import Project, Site, Building, Storey, Space, Product


def load_product(ifc_product, parent):
    product = Product(
        parent=parent,
        name=ifc_product.Name,
        global_id=ifc_product.GlobalId
    )
    return product


def load_space(ifc_space, storey):
    space = Space(
        storey=storey,
        name=ifc_space.Name,
        global_id=ifc_space.GlobalId,
        long_name=ifc_space.LongName,
        description=ifc_space.Description
    )
    for ifc_product in get_related_elements(ifc_space):
        load_product(ifc_product, space)
    return space


def load_storey(ifc_storey, building):
    assert ifc_storey.is_a('IfcBuildingStorey')
    storey = Storey(
        building=building,
        name=ifc_storey.Name,
        global_id=ifc_storey.GlobalId,
        long_name=ifc_storey.LongName,
        description=ifc_storey.Description,
        elevation=ifc_storey.Elevation)
    for ifc_data in get_related_objects(ifc_storey):
        load_space(ifc_data, storey)
    for ifc_product in get_related_elements(ifc_storey):
        load_product(ifc_product, storey)
    return storey


def load_building(ifc_building, site):
    assert ifc_building.is_a('IfcBuilding')
    building = Building(
        site=site,
        name=ifc_building.Name,
        global_id=ifc_building.GlobalId,
        long_name=ifc_building.LongName,
        description=ifc_building.Description,
        elevation_of_terrain=ifc_building.ElevationOfTerrain,
        elevation_of_ref_height=ifc_building.ElevationOfRefHeight
    )
    for ifc_product in get_related_elements(ifc_building):
        load_product(ifc_product, building)
    for ifc_data in get_related_objects(ifc_building):
        load_storey(ifc_data, building)
    return building


def load_site(ifc_site, project):
    assert ifc_site.is_a('IfcSite')
    site = Site(
        project=project,
        global_id=ifc_site.GlobalId,
        name=ifc_site.Name,
        long_name=ifc_site.LongName,
        description=ifc_site.Description,
        elevation=ifc_site.RefElevation
    )
    for ifc_building in get_related_objects(ifc_site):
        load_building(ifc_building, site)
    return site


def load_project(filename):
    ifc_file = ifcopenshell.open(filename)
    ifc_project = ifc_file.by_type('IfcProject')[0]
    project = Project(
        global_id=ifc_project.GlobalId,
        name=ifc_project.Name,
        long_name=ifc_project.LongName,
        filename=filename,
        description=ifc_project.Description
    )
    for ifc_site in ifc_file.by_type('ifcsite'):
        load_site(ifc_site, project)
    return project
