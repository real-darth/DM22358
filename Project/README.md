# Project

## Documentation

For in depth documentation please refer to the doxygen in the 'Doxygen' folder, or the report.

## Installation
Create a virtual enviorment and activate it:
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

### Install CuPy
If you want to run the GPU optimization, the correct version of CuPy needs to be installed. This version below is for running with CUDA (Nvidia GPU):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

CUDA Toolkit can be downloaded [here](https://developer.nvidia.com/cuda-12-0-0-download-archive).

### To build Cython
Check Cython is installed
```
cython --version
```
Then run
```
python setup.py build_ext --inplace
```

## Running Unit Tests
To run the unit-tests, execute the following command
```
python -m pytest
```
or
```bash
pytest simulate_flocking_test.py
```

## Running Benchmarks
### Benchmark tool
To run the benchmark tool, to benchmark using line-profiler, cProfile or memory profiler run:
```
python benchmark.py
```
Instructions will be shown when running the script. Benchmarks are stored in the `benchmark` directory.

### Comparision benchmark
To run the large benchmark that compares the different optimizations (plots them on a graph) run the following:
```
python compare_implementation.py
```
Make sure to edit the script before to set the ranges of data points to plot within.

## Useful vs-code configuration
Install the extensions `ms-python.black-formatter`, `ms-python.python` and `ms-python.vscode-pylance`

Moreover, you are encouraged to install the pre-commit hooks, so that black and the flake8 run before every commit:
```bash
pre-commit install
```
