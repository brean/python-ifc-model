import json


def export(project, filename=None):
    if not filename:
        filename = project.filename[:-4] + '.json'
    with open(filename, 'w') as jf:
        json.dump(project.to_dict(), jf, indent=2)
