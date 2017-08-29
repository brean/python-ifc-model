idea: remove all classes and create some more generic items, maybe with a description and some mapping to get some shortcuts (e.g. just get all polylines if we just want to draw)
ifcopenshell already defines the ifc-model structure - I could create a JSON-structure iterating over all items, using something like  https://gist.github.com/brean/872b32ce3617a1a25e1c245d7b75df35
(maybe in combination with a whitelist to keep the filesize down, like this)
```python
KNOWN_ITEMS = {
    'IfcBuilding': {'name': 'Name'}
}

class IfcElement(dict):
    def __init__(parent):
        self.parent = parent
    
    def from_ifc(ifc_data):
        self.ifc_data = ifc_data
        ifc_type = ifc_data.is_a()
        if ifc_type in KNOWN_ITEMS:
            ifc_items = KNOWN_ITEMS[ifc_type]
            for k, v in ifc_items.items():
                self[k] = ifc_items[v]
```
