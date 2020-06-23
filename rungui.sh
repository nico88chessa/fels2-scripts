#!/bin/sh

PYTHONPATH=$(pwd)/fels2scripts
echo "PYTHONPATH=$PYTHONPATH"
$(PYTHONPATH=$(pwd)/fels2scripts ./venv/bin/python $PYTHONPATH/gui/fels2-gui.py)
