"""
this module mainly exposes a dictionary 'problems'
of the form problem_name -> problem_function

each problem function returns a dict with 2 keys
they should return a dict with
- data: a numpy array
- solutions: purpusefully left loosely specified as a collection of solutions
  e.g. may be a list of lists, a numpy array, etc..
  tentatively we return them in the same order as the
  original article with the S heuristic

also there a are 3 helper tools that help canocalize solutions for comparison
"""

from functools import partial
from importlib import resources

import numpy as np
import pandas as pd

DTYPE_FOR_ARRAY = bool


# canonicalize solutions
def canonical_1(solution):
    """
    how to canonicalize one solution
    """
    return tuple(sorted(solution))

def canonical_s(solutions):
    """
    apply canonical_1 on all solutions, as a list in the original order
    """
    return [canonical_1(solution) for solution in solutions]

def canonical(solutions):
    """
    same but also turn into a set
    """
    return set(canonical_s(solutions))


# locate and load packaged files
def load_npy(filename):
    p = resources.files("exact_cover_samples.data").joinpath(f"{filename}.npy")
    return np.load(str(p))

def load_csv(filename):
    p = resources.files("exact_cover_samples.data").joinpath(f"{filename}.csv")
    try:
        return pd.read_csv(p, header=None).to_numpy()
    except FileNotFoundError:
        print(f"file {filename}.csv not found - returning empty dataframe")
        return np.array([[0]])


problems = {}

# a decorator to store functions in problems as we go
def add_to_problems(shortname, function):
    """
    add a problem to the problems dict
    """
    name = function.__name__.replace("_", "-")
    def wrapped():
        raw = function()
        raw['name'] = name
        raw['shortname'] = shortname
        return raw
    problems[shortname] = wrapped
    return wrapped


# a specialized version where the data is stored in the data/ folder
def add_to_problems_from_file(shortname, function):
    """
    same as add_to_problems, with the data loaded from the data/ folder
    in files named
    filename.csv
    and
    filename-solutions.csv
    """
    name = function.__name__.replace("_", "-")
    def wrapped():
        return dict(
            data=load_csv(name),
            solutions=load_csv(f"{name}-solutions"),
            name=name,
            shortname=shortname,
        )
    problems[shortname] = wrapped
    return wrapped

# may be useful to test the algorithm on a trivial problem
# since this is the one illustrated in the original article
@partial(add_to_problems, "knuth2000")
def knuth_original():
    to_cover = np.array(
        [
            [0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 1],
        ]
    )
    return {"data": to_cover, "solutions": [(0, 3, 4)]}


@partial(add_to_problems, "knuth2019")
def knuth_vol4():
    text = """
0010100
1001001
0110010
1001010
0100001
0001101
"""

    data = np.array([[int(c) for c in line] for line in text.strip().split("\n") if line])
    return {"data": data, "solutions": [(0, 3, 4)]}


# same problem in fact, but expressed a little differently
# https://en.wikipedia.org/wiki/Exact_cover#Detailed_example
@partial(add_to_problems, "wikip")
def detailed_wikipedia():
    sets = [
        {1, 4, 7},
        {1, 4},  # <- 1
        {4, 5, 7},
        {3, 5, 6},  # <- 3
        {2, 3, 6, 7},
        {2, 7},  # <- 5
    ]
    return dict(
        data=np.array(
            [[1 if i in s else 0 for i in range(1, 8)] for s in sets],
            dtype=DTYPE_FOR_ARRAY,
        ),
        solutions=[(1, 3, 5)],
    )


@partial(add_to_problems, "brtf1")
def bruteforce1():
    to_cover = [
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY), solutions=[(0, 1, 2), (3, 4, 5)]
    )


@partial(add_to_problems, "brtf2")
def bruteforce2():
    to_cover = [
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions=canonical(
            [
                (0, 1, 2),
                (0, 1, 8),
                (0, 7, 2),
                (0, 7, 8),
                (4, 5, 3),
                (6, 1, 2),
                (6, 1, 8),
                (6, 7, 2),
                (6, 7, 8),
            ]
        ),
    )


@partial(add_to_problems, "brtf3")
def bruteforce3():
    to_cover = [
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions=canonical(
            [
                (0, 1, 2),
                (0, 1, 8),
                (0, 7, 2),
                (0, 7, 8),
                (4, 5, 3),
                (4, 5, 9),
                (4, 11, 3),
                (4, 11, 9),
                (6, 1, 2),
                (6, 1, 8),
                (6, 7, 2),
                (6, 7, 8),
                (10, 5, 3),
                (10, 5, 9),
                (10, 11, 3),
                (10, 11, 9),
            ]
        ),
    )


@partial(add_to_problems, "brtf30")
def bruteforce3_odd_zeros():
    p = bruteforce3()
    d, s = p["data"], p["solutions"]
    r, c = d.shape
    # add same area of 0s on the right hand side of d
    d1 = np.hstack((d, np.zeros(d.shape, dtype=d.dtype)))
    # reshape it - each gets folded in 2
    # so we end up with all the odd rows being 0
    d2 = d1.reshape((-1, c))
    # non empty rows are now 0 2 4, so twice the original index
    s = {tuple(map(lambda i: i * 2, t)) for t in s}
    return dict(data=d2, solutions=s)


@partial(add_to_problems, "brtf31")
def bruteforce3_even_zeros():
    p = bruteforce3()
    d, s = p["data"], p["solutions"]
    r, c = d.shape
    # add same area of 0s on the left hand side of d
    d1 = np.hstack((np.zeros(d.shape, dtype=d.dtype), d))
    # reshape it - each gets folded in 2
    # so we end up with all the even rows being 0
    d2 = d1.reshape((-1, c))
    # non empty rows are now 1 3 5, so twice the original index + 1
    s = {tuple(map(lambda i: i * 2 + 1, t)) for t in s}
    return dict(data=d2, solutions=s)


@partial(add_to_problems, "lgfd3")
def langford3():
    raw = [
        "1s1s3",
        "1s2s4",
        "1s3s5",
        "1s4s6",
        "2s1s4",
        "2s2s5",
        "2s3s6",
        "3s1s5",
        "3s2s6",
    ]
    to_cover = np.zeros((len(raw), 3*3), dtype=bool)
    for i, line in enumerate(raw):
        j, si, sj = [int(x) for x in line.split("s")]
        j = j-1
        to_cover[i, j] = True
        to_cover[i, 3 + si-1] = True
        to_cover[i, 3 + sj-1] = True
    return dict(
        data=to_cover,
        solutions=[(2, 4, 8), (1, 6, 7)],
    )

# problem originally based on solving the trivial problem
# of arranging 2 identical triminos on a 3x3 board

#    +--+
#    |  |
# +--+--+
# |  |  |
# +--+--+

# +--+--+--+
# |xx|  |xx|
# +--+--+--+
# |  |  |  |
# +--+--+--+
# |xx|  |  |
# +--+--+--+


# this problem has 2 solutions
# (5, 13) and (6, 12)
@partial(add_to_problems, "strim")
def small_trimino():
    to_cover = [
        [1, 0, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0],  # <- 5
        [1, 0, 0, 0, 0, 1, 1, 1],  # <- 6
        [0, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 1, 1, 1, 1, 0, 0, 0],  # <- 12
        [0, 1, 0, 0, 0, 1, 1, 1],  # <- 13
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions=[(5, 13), (6, 12)],
    )


@partial(add_to_problems, "strimf")
def small_trimino_from_file():
    return dict(
        data=load_npy("small-trimino"),
        solutions=[(5, 13), (6, 12)],
    )


# pentominos - the function name is to locate the data file

@partial(add_to_problems_from_file, "p3x20")
def pentominos_3_20(): pass

@partial(add_to_problems_from_file, "p4x15")
def pentominos_4_15(): pass

@partial(add_to_problems_from_file, "p5x12")
def pentominos_5_12(): pass

@partial(add_to_problems_from_file, "p6x10")
def pentominos_6_10(): pass

@partial(add_to_problems_from_file, "p2x5x6")
def pentominos_2_5_6(): pass

# 8x8 with a 2x2 square removed in the center
@partial(add_to_problems_from_file, "p8x8")
def pentominos_8_8(): pass

# 8x9 with 2x2 squares removed in the corners
@partial(add_to_problems_from_file, "p8x9")
def pentominos_8_9(): pass



def print_problem(problem, header=False):
    name = problem["name"]
    shortname = problem["shortname"]
    data = problem["data"]
    solutions = problem["solutions"]
    if header:
        print(f"{' '+shortname+' ':=^50}")
        repeat = ""
    else:
        repeat = f"short={shortname} "
    print(
            f"{repeat}"
            f"size = {data.shape}, "
            f" {len(canonical(solutions))} solutions"
            f" full_name={name}")


def summary(filter=None):
    """
    convenience to display a summary of all problems
    """
    if not filter:
        print(f"{8*'-'} we have a total of {len(problems)} problems")
    else:
        print(f"the problems whose name contains '{filter}' are:")
    for shortname, function in problems.items():
        problem = function()
        name = problem['name']
        if filter is not None and filter not in name and filter not in shortname:
            continue
        print_problem(problem, header=True)

def spot(needle):
    """
    returns the first problem instance whose name or shortname contains needle
    """
    for shortname, function in problems.items():
        problem = function()
        name = problem['name']
        if needle in name or needle in shortname:
            return problem


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", "--list", action="store_true")
    parser.add_argument("problem", nargs='?', default=None)
    args = parser.parse_args()
    if args.list:
        if args.problem:
            summary(args.problem)
        else:
            summary()
    elif args.problem:
        print_problem(spot(args.problem))
    else:
        summary()
