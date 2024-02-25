# Project

## Installation
### Linux/MacOX
```bash
python3.9 -m venv venv  
source venv/bin/activate
```

### Windows
```bash
python -m venv venv  
source venv/scripts/activate
```

For installing dependecies do:

```bash
pip install .
```

And for developmnet dependencies (needed to run tests) do:
```bash
pip install ".[dev]"
```

### To build Cython
Check Cython is installed
```
cython --version
```
Then run
```
python setup.py build_ext --inplace
```

## Test
To run the unit-tests, execute the following command
```
python -m pytest
```

Moreover, you are encouraged to install the pre-commit hooks, so that black and the flake8 run before every commit:
```bash
pre-commit install
```

## Useful vs-code configuration
Install the extensions `ms-python.black-formatter`, `ms-python.python` and `ms-python.vscode-pylance`


