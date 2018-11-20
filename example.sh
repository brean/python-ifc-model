#!/bin/bash
if [ ! -f buildings/AC20-FZK-Haus.ifc ]; then
    wget -O buildings/AC20-FZK-Haus.ifc www.ifcwiki.org/images/e/e3/AC20-FZK-Haus.ifc
fi
pipenv run python example.py
