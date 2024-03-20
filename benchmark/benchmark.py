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

# # a decorator that catches exceptions and returns a special result
# def protect_exception(libname, version, fn):
#     def wrapped(name, problem, run_index, n):
#         try:
#             return fn(name, problem, run_index, n)
#         except Exception as e:
#             return dict(
#                 library=libname, version=version,
#                 problem=name, run=run_index,
#                 nb_solutions=0, finite=True, time=0.0, error=str(e))
#     return wrapped


class Library:
    def run(self, problem, size):
        raise NotImplementedError

class ExactCover(Library):
    def __init__(self):
        self.name = "exact-cover"
        self.version = exact_cover_version
    def run(self, problem, size):
        if size == 1:
            r = [get_exact_cover(problem["data"])]
        elif size == 0:
            r = get_exact_covers(problem["data"])
        else:
            r = get_exact_covers(problem["data"], max_count=size)
        return len(r)

class ExactCoverPy(Library):
    def __init__(self):
        self.name = "exact-cover-py"
        self.version = exact_cover_py_version
    def run(self, problem, size):
        solutions = exact_covers(problem["data"])
        if size > 0:
            counter = size
            for _ in range(size):
                next(solutions)
        elif size == 0:
            counter = 0
            for _ in solutions:
                counter += 1
        return counter

class XCover(Library):
    def __init__(self):
        self.name = "xcover"
        self.version = xcover_version
    def run(self, problem, size):
        solutions = covers_bool(problem["data"])
        if size > 0:
            counter = size
            for _ in range(size):
                next(solutions)
        elif size == 0:
            counter = 0
            for _ in solutions:
                counter += 1
        return counter

ALL_LIBS = [ExactCover(), ExactCoverPy(), XCover()]


def run_library(lib, problem, run_index, size):
    requested = size
    expected = len(problem["solutions"])
    if size != 0:
        expected = min(size, expected)
    start = time.perf_counter()
    try:
        computed = lib.run(problem, size)
        end = time.perf_counter()
        result = dict(
            library=lib.name, version=lib.version,
            problem=problem['shortname'], run=run_index,
            requested=requested, expected=expected, computed=computed,
            time=end - start, error="")
        if computed != expected:
            result["error"] = f"expected {expected} but got {computed}"
        return result
    except Exception as e:
        return dict(
            library=lib.name, version=lib.version,
            problem=problem['shortname'], run=run_index,
            requested=requested, expected=expected, computed=-1,
            time=0.0, error=str(e))



def run_once(run_index, full=False):
    # the various configurations we try
    # sizes means how many solutions we want to compute
    # with 0 meaning all of them
    # passing full=False will skip the 0 case
    sizes = [1, 50]
    if full:
        sizes.append(0)
    problems = ecs.problems
    for problem_fn in problems.values():
        problem = problem_fn()
        print(f"=== problem {problem['name']}")
        for lib in ALL_LIBS:
            print(f"= library {lib.name}")
            store_records(
                [run_library(lib, problem, run_index, size) for size in sizes])

def main():
    parser = ArgumentParser()
    parser.add_argument("-r", "--repeat", type=int, default=1)
    parser.add_argument("-f", "--full", action="store_true", default=False)
    args = parser.parse_args()
    for run_index in range(args.repeat):
        run_once(run_index, args.full)

if __name__ == "__main__":
    main()
