class Product(object):
    def __init__(self, parent, name, global_id=None):
        self.parent = parent
        self.parent.products.append(self)
        self.name = name
        self.global_id = global_id

    def to_dict(self):
        data = self.__dict__
        del data['parent']
        return data


class Wall(Product):
    def __init__(self, parent, name, width, length, height, global_id=None):
        super().__init__(parent, name, global_id)
        self.width = width
        self.length = length
        self.height = height


class Door(Product):
    def __init__(self, parent, name, global_id=None):
        super().__init__(parent, name, global_id)


class Window(Product):
    def __init__(self, parent, name, global_id=None):
        super().__init__(parent, name, global_id)
