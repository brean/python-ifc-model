#!/bin/bash
wget https://github.com/IfcOpenShell/IfcOpenShell/releases/download/v0.5.0-preview2/ifcopenshell-python35-master-9ad68db-linux64.zip
unzip ifcopenshell-python35-master-9ad68db-linux64.zip
rm ifcopenshell-python35-master-9ad68db-linux64.zip
pipenv install .
