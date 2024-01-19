# DM2358
HPC course, assignments and project
## Installation
```bash
python3.9 -m venv venv  
source venv/bin/activate
```

For installing dependecies do 

```bash
pip install .
```

And for developmnet dependencies do :
```bash
pip install ".[dev]"
```

Moreover, you are encouraged to install the pre-commit hooks, so that black and the flake8 run before every commit:
```bash
pre-commit install
```

## Useful vs-code configuration
Install the extensions `ms-python.black-formatter`, `ms-python.python` and `ms-python.vscode-pylance

