from ifc_model.model import *
from ifc_model.ifcopenshell.exporter import export as ifcopenshell_export


def main():
    p = Project(
        name='Test Building',
        filename='test.ifc')
    address = Address(
        address_lines=['12 Somewhere Road'],
        town='Nowhere',
        country='UnknownLand'
    )
    site = Site(
        p,
        name='Test Site',
        address=address,
        longitude=0.12345,
        latitude=1.2345)
    building = Building(
        site,
        name='Test Building',
        address=address,
        description='some test building')
    ground_floor = Storey(
        building,
        name='Ground Floor'
    )
    ifcopenshell_export(p)


if __name__ == '__main__':
    main()
