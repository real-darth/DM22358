# Assignment 1

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
