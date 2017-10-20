- idea: remove all classes and create some more generic items, maybe with a description and some mapping to get some shortcuts (e.g. just get all polylines if we just want to draw)
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


```python
# alternative:
class IfcProduct():
    def __init__(self, parent):
        self.parent = parent
        self.member = {
            'name': 'str',
            'id': 'func' # special case
        }
    
    def from_ifc(ifc_data):
        pass

class Building(IfcProduct):
    def __init__(self, parent):
        super(Building, self).__init__(parent)

ifc_map = {
    Building: ['IfcBuilding']
}

class Parser(object):
    def from_ifc(ifc_data, parent):
        self.ifc_data = ifc_data
        ifc_type = ifc_data.is_a()
        for cls,ifc_types in ifc_map.items():
            if ifc_type in ifc_types:
               cls(parent) # get the parent, call from_ifc recursively
               cls.from_ifc(ifc_data)
               
```
- idea: configure which data to export to JSON/configure structure to keep the json-file small (if you only need the product names and ids for example but not their representation)
