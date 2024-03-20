# benchmarks

comparing the performance of different implementations of D. Knuth's exact cover
algorithm, a.k.a. Algorithm X a.k.a. Dancing Links

## Implementations

- `pip install exact-cover`  
  from `https://github.com/jwg4/exact_cover`  
  a C implementation with Python bindings

- `pip install xcover`  
  from `https://github.com/johnrudge/xcover`  
  a Python/numba

- `pip install exact_cover_py`
  from the local repo `https://github.com/parmentelat/exact-cover-py`  
  a pure Python implementation

## Requirements

```bash
cd .. # at the root of the repo
pip install -e .[benchmarks]
cd benchmark
```

## Running the benchmarks

```bash
# still in benchmark/
python benchmark.py -r 2 -f
```

options:

- `--runs` to specify the number of runs (default 1)
- `--full` to run with no limit (othrwise will go for 1 and 50 solutions only)
- `--algo` to specify the algorithm to run (default all)

## Results

go into `results.csv`

- library: the library used
- version: the library version
- problem: a standardized problem name
- run: the run number; 0 means the first run, it may be useful to discard
  the first run as it may include some warmup time
- requested: how many solutions were requested
- expected: how many solutions were expected
- computed: how many solutions were computed
- finite: if True, it means the caller has asked for a finite number of solutions
  otherwise all solutions were returned
- time: the time it took to solve the problem, in seconds
- error: a string that may contain:
  - if the library raised an exception, it is reported here
  - if a mismatch was detected between the solutions, it is reported here

## Figures

see jupyter notebook `postprocess-nb.py`

which is also runnable as a script `python postprocess-nb.py`
and will produce `results.png` and `results.svg`
