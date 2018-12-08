class Space(object):
    def __init__(self, storey, name, global_id=None, description=None,
                 long_name=None):
        self.storey = storey
        self.storey.spaces.append(self)
        self.name = name
        self.global_id = global_id
        self.long_name = long_name
        self.description = description
        self.products = []

    def to_dict(self):
        data = self.__dict__
        del data['storey']
        return data
