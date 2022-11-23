:: Script för att initializera ens system för dungeons of kwargs
pip install setuptools -U
pip install -r requirements.txt
cd dependencies/pygame
py -m buildconfig --download
pip install .