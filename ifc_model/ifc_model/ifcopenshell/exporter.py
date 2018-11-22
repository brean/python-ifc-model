import uuid
import time
import tempfile
import ifcopenshell
from ifc_model.data.template import template_data

ORIGIN = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.


def create_guid():
    """
    create an IFCOpenShell-guid

    Returns
    -------
    randomly generated guid from ifcopenshell
    """
    return ifcopenshell.guid.compress(uuid.uuid1().hex)


def create_ifc_axis2placement(ifcfile, point=ORIGIN, dir1=Z, dir2=X):
    """
    Creates an IfcAxis2Placement3D from Location, Axis and RefDirection
    specified as Python tuples

    """
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    return ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)


def create_ifc_local_placement(ifc_file, point=ORIGIN, dir1=Z, dir2=X,
                               relative_to=None):
    """
    Creates an IfcLocalPlacement from Location, Axis and RefDirection,
    specified as Python tuples, and relative placement


    Parameters
    ----------
    ifc_file : ifcopenshell.file
        instance of an ifc open shell file
    point : tuple
        x,y,z position of the placement relative to relative_to
    dir1 : tuple
        x,y,z of direction (should be Z-axis, so 0,0,1)
    dir2 : tuple
        x,y,z of direction (should be X-axis, so 1,0,0)
    relative_to : IfcLocalPlacement(
        ifc-element that this location is relative to
    """
    axis2placement = create_ifc_axis2placement(ifc_file, point, dir1, dir2)
    return ifc_file.createIfcLocalPlacement(
        relative_to, axis2placement)


def ifc_from_template(project, meta=None):
    """
    create small ifc file with some basic data in it as starting point.

    Parameters
    ----------
    project : ifc_model.model.project.Project
        project that stores the all information about buildings (root node)
    meta : dict
        contains meta information about the ifc project
        (creation-timestamp, organization, application, filename, ...)

    Returns
    -------
    IFCOpenShell file instance
    """
    timestamp = time.time()
    meta = {
        'timestamp': timestamp,
        'timestring': time.strftime(
            "%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp)),
        'creator': project.creator,
        'organization': project.organization,
        'application': 'ifc_model',
        'application_version': '0.1',
        'project_globalid': create_guid(),
        'project_name': project.name,
        'filename': project.filename
    } if not meta else meta
    template = template_data % meta
    temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
    with open(temp_filename, "wb") as f:
        f.write(template.encode())
    return ifcopenshell.open(temp_filename)


def get_id(elem):
    return elem.global_id if elem.global_id else create_guid()


def get_address(ifc_file, elem):
    return export_address(ifc_file, elem.address) if elem.address else None


def create_ifc_postal_address(
        ifc_file, internal_location='', address_lines=None, postal_box='',
        town='', region='', postal_code='', country=''):
    return ifc_file.createIfcPostalAddress(
        InternalLocation=internal_location,
        AddressLines=address_lines,
        PostalBox=postal_box,
        Town=town,
        Region=region,
        PostalCode=postal_code,
        Country=country
    )


def export_product(ifc_file, product, ifc_refs):
    pass


def export_space(ifc_file, space, ifc_refs):
    ifc_file.createIfcSpace(

    )
    for product in space.products:
        export_product(ifc_file, product, ifc_refs)


def export_storey(ifc_file, storey, ifc_refs):
    storey_placement = create_ifc_local_placement(
        ifc_file, relative_to=ifc_refs['building_placement'])
    ifc_storey = ifc_file.createIfcBuildingStorey(
        GlobalId=get_id(storey),
        OwnerHistory=ifc_refs['owner_history'],
        Name=storey.name,
        Description=storey.description,
        ObjectType=None,
        ObjectPlacement=storey_placement,
        Representation=None,
        LongName=storey.long_name,
        CompositionType="ELEMENT",
        Elevation=storey.elevation)
    for space in storey.spaces:
        export_space(ifc_file, space, ifc_refs)
    for product in storey.products:
        export_product(ifc_file, product, ifc_refs)
    return ifc_storey


def export_building(ifc_file, building, ifc_refs):
    ifc_refs['building_placement'] = create_ifc_local_placement(
        ifc_file, relative_to=ifc_refs['site_placement'])

    ifc_building = ifc_file.createIfcBuilding(
        GlobalId=get_id(building),
        OwnerHistory=ifc_refs['owner_history'],
        Name=building.name,
        Description=building.description,
        # ObjectType=None,
        ObjectPlacement=ifc_refs['building_placement'],
        # Representation=None,
        LongName=building.long_name,
        CompositionType="ELEMENT",
        ElevationOfRefHeight=building.elevation_of_ref_height,
        ElevationOfTerrain=building.elevation_of_terrain,
        BuildingAddress=get_address(ifc_file, building))
    for storey in building.storeys:
        export_storey(ifc_file, storey, ifc_refs)
    for product in building.products:
        export_product(ifc_file, product, ifc_refs)
    return ifc_building


def export_address(ifc_file, address):
    create_ifc_postal_address(
        ifc_file,
        internal_location=address.internal_location,
        address_lines=address.address_lines,
        postal_box=address.postal_box,
        town=address.town,
        region=address.region,
        postal_code=address.postal_code,
        country=address.country
    )


def export_site(ifc_file, site, ifc_refs):
    ifc_refs['site_placement'] = create_ifc_local_placement(ifc_file)
    ifc_site = ifc_file.createIfcSite(
        GlobalId=get_id(site),
        OwnerHistory=ifc_refs['owner_history'],
        Name=site.name,
        Description=site.description,
        # ObjectType=None,
        ObjectPlacement=ifc_refs['site_placement'],
        # Representation=None,
        LongName=site.long_name,
        CompositionType='ELEMENT',
        # TODO: create IfcCompoundPlaneAngleMeasure
        # RefLatitude=site.latitude,
        # RefLongitude=site.longitude,
        RefElevation=site.elevation,
        LandTitleNumber='',
        SiteAddress=get_address(ifc_file, site)
    )
    for building in site.buildings:
        export_building(ifc_file, building, ifc_refs)
    return ifc_site


def export(project, meta=None):
    if not project.filename:
        raise Exception('Please provide a file name for the project!')
    ifc_file = ifc_from_template(project, meta)
    ifc_refs = {
        'owner_history': ifc_file.by_type("IfcOwnerHistory")[0]
    }
    for site in project.sites:
        export_site(ifc_file, site, ifc_refs)
    ifc_file.write(project.filename)
