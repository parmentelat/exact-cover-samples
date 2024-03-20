"""
see README.md for more details
"""

import time
from pathlib import Path
from argparse import ArgumentParser
from functools import partial

import pandas as pd


# samples
import exact_cover_samples as ecs

# exact-cover-py
from exact_cover_py import exact_covers, __version__ as exact_cover_py_version

# exact cover
# from exact_cover import get_exact_cover, __version__ as exact_cover_version
from exact_cover import get_exact_cover, get_all_solutions as get_exact_covers
exact_cover_version = "1.4.0a1"
print(f"WARNING using hard-wired version {exact_cover_version=}")

# xcover
from xcover import covers_bool, __version__ as xcover_version


# accumulate results in this file
RESULTS = "results.csv"


def store_records(records):
    if Path(RESULTS).exists():
        past_records = pd.read_csv(RESULTS)
    else:
        past_records = pd.DataFrame()
    new_results = pd.DataFrame(records)
    pd.concat([past_records, new_results], ignore_index=True).to_csv(RESULTS, index=False)

# a decorator that catches exceptions and returns a special result
def protect_exception(libname, version, fn):
    def wrapped(name, problem, run_index, n):
        try:
            return fn(name, problem, run_index, n)
        except Exception as e:
            return dict(
                library=libname, version=version,
                problem=name, run=run_index,
                nb_solutions=0, finite=True, time=0.0, error=str(e))
    return wrapped


# only return first solution
@partial(protect_exception, "exact-cover", exact_cover_version)
def run_exact_cover(name, problem, run_index, n):
    start = time.perf_counter()
    finite = (n > 0)
    if n == 1:
        solutions = [get_exact_cover(problem["data"])]
    elif n >= 0:
        max_count = None if n == 0 else n
        solutions = [get_exact_covers(problem["data"], max_count=max_count)]
    nb_solutions = len(solutions)
    end = time.perf_counter()
    return dict(
        library='exact-cover', version=exact_cover_version,
        problem=name, run=run_index,
        nb_solutions=1, finite=True, time=end - start,
        error="")


@partial(protect_exception, "exact-cover-py", exact_cover_py_version)
def run_exact_cover_py(name, problem, run_index, n):
    start = time.perf_counter()
    solutions = exact_covers(problem["data"])
    finite = (n > 0)
    if n > 0:
        counter = n
        for _ in range(n):
            next(solutions)
    elif n == 0:
        counter = 0
        for _ in solutions:
            counter += 1
    end = time.perf_counter()
    return dict(
        library='exact-cover-py', version=exact_cover_py_version,
        problem=name, run=run_index,
        nb_solutions=counter, finite=finite, time=end - start,
        error="")
    # print(f"time 5x12 - {n} solutions {end - start:.6f} s")


@partial(protect_exception, "xcover", xcover_version)
def run_xcover(name, problem, run_index, n):
    start = time.perf_counter()
    solutions = covers_bool(problem["data"])
    finite = (n > 0)
    if n > 0:
        counter = n
        for _ in range(n):
            next(solutions)
    elif n == 0:
        counter = 0
        for _ in solutions:
            counter += 1
    end = time.perf_counter()
    return dict(
        library='xcover', version=xcover_version,
        problem=name, run=run_index,
        nb_solutions=counter, finite=finite, time=end - start,
        error="")


def run_once(run_index, full=False):
    # the various configurations we try
    # sizes means how many solutions we want to compute
    # with 0 meaning all of them
    # passing full=False will skip the 0 case
    sizes = [1, 50]
    if full:
        sizes.append(0)
    problems = ecs.problems
    for name, problem_fn in problems.items():
        problem = problem_fn()
        print(f"=== problem {name}")
        print("exact-cover")
        store_records(
            [run_exact_cover(name, problem, run_index, size) for size in sizes])
        print("xcover")
        store_records(
            [run_xcover(name, problem, run_index, size) for size in sizes])
        print("exact-cover-py")
        store_records(
            [run_exact_cover_py(name, problem, run_index, size) for size in sizes])


def main():
    parser = ArgumentParser()
    parser.add_argument("-r", "--repeat", type=int, default=1)
    parser.add_argument("-f", "--full", action="store_true", default=False)
    args = parser.parse_args()
    for run_index in range(args.repeat):
        run_once(run_index, args.full)

if __name__ == "__main__":
    main()
