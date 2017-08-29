idea: remove all classes and create some more generic items, maybe with a description and some mapping to get some shortcuts (e.g. just get all polylines if we just want to draw)
ifcopenshell already defines the ifc-model structure
```python
class IfcElement(object):
    def __init__(parent):
        self.parent = parent
    
    def from_ifc(ifc_data):
        self.ifc_data = ifc_data
        
```
