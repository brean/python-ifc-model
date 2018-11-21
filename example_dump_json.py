#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ifc_model.ifcopenshell.importer import load_project
from ifc_model.json.exporter import export


def main():
    for building_file in os.listdir('buildings'):
        if not building_file.endswith('.ifc'):
            continue
        ifc_file = os.path.join('buildings', building_file)
        json_file = os.path.join('out', building_file[:-4]+'.json')
        project = load_project(ifc_file)
        export(project, filename=json_file)


if __name__ == '__main__':
    main()
