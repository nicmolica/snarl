export PYTHONPATH=$(cd ../../../ && pwd)$PYTHONPATH
coverage run -m --omit="*/Lib/*,*/Tests/*" unittest discover Tests
