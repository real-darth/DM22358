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
Install the extensions `ms-python.black-formatter`, `ms-python.python` and `ms-python.vscode-pylance`



## Bonus exercise
```
usage: main.py [-h] [-i INTERVAL] [--plot] [-o OUTPUT] script

Measure the CPU usage of a python script per core

positional arguments:
  script                Script to measure CPU usage of

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Interval at which the CPU usage is to be measured in seconds
  --plot                Plot the CPU usage of each core
  -o OUTPUT, --output OUTPUT
                        Write the CPU usage of each core to a file
```

For using with the JuliaSet use:
```bash
python bonus/main.py --plot Task1/JuliaSet.py
```
