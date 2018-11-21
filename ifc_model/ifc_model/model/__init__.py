"""
these are just the basic models as python classes.
The data is stored as base data types.
They do not need anything from IFCOpenShell or any other IFC-library
"""

from .project import Project
from .site import Site, Address
from .building import Building
from .storey import Storey
from .space import Space
from .product import Product, Wall, Door, Window

