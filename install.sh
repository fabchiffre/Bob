#/bin/sh

wget https://pypi.python.org/packages/source/b/bitarray/bitarray-0.8.1.tar.gz

tar xvfz bitarray-0.8.1.tar.gz
cd bitarray-0.8.1
python setup.py install --user

export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
