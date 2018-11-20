#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from ifc_model.project import Project


def json_dump(ifc_file, json_file):
    project = Project()
    project.open_ifc(ifc_file)
    data = project.to_json()
    json.dump(
        project.to_json(),
        open(json_file, 'w'),
        indent=2,
        sort_keys=True
    )

def main():
    for building_file in os.listdir('buildings'):
        if not building_file.endswith('.ifc'):
            continue
        json_dump(
            os.path.join('buildings', building_file),
            os.path.join('out', building_file[:-4]+'.json')
        )


if __name__ == '__main__':
    main()
