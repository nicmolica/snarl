export PYTHONPATH=$(cd ../../../ && pwd)$PYTHONPATH
coverage run -m --omit="*/Lib/*,*/Tests/*,*/__init__.py" unittest discover Tests
# just run tests: 
# python3 -m unittest discover Tests
