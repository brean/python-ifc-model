import os
from ifc_model.model import *
from ifc_model.ifcopenshell.exporter import export as ifcopenshell_export


def main():
    p = Project(
        name='Test Building',
        filename=os.path.join('out', 'test.ifc'))
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
    living_room = Space(
        ground_floor,
        name='Living Room'
    )
    # inner size of the room in meter
    height = 2.8
    width = 4.0
    length = 5.0
    # 10 cm wall width for all 4 walls around the room
    wall_width = 0.1
    left = Wall(living_room,
        name='left wall',
        width=wall_width,
        length=length,
        height=height)
    top = Wall(living_room,
        name='top wall',
        width=wall_width,
        length=width,
        height=height)

    bath = Space(
        ground_floor,
        name='Bath'
    )
    floor = Space(
        ground_floor,
        name='Floor'
    )
    ifcopenshell_export(p)


if __name__ == '__main__':
    main()
