export PYTHONPATH=$(cd ../../ && pwd)$PYTHONPATH
pyinstaller --onefile testState.py
