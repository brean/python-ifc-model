# IFC model
wrapper around [IfcOpenShell](http://ifcopenshell.org/) to read and write data 
from IFC, so it can be for example exported into JSON-format for easier access 
across different platforms.
It also provides an easy API to generate general objects like walls, doors and 
windows programmatically see example_create_building.py.

See [ifc-blender](https://github.com/brean/ifc_blender) for a usage example.

# IMPORTANT!
After loading an ifc-file it will be parsed into an own structure that will be 
written from a template file. the resulting ifc-file can look quite different 
from the original and some data might get lost!

I strongly recommend you to keep a backup of the original IFC-file and not 
overwrite the file with the output of the exporter!

# Note
This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/).

# Documentation
We use [NumPydoc](https://numpydoc.readthedocs.io)
