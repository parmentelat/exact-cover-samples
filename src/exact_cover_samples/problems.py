"""
all functions whose name contains '_problem'
are made part of the ALL_PROBLEMS list

they should return a dict with
- data: a numpy array
- solutions: purpusefully left loosely specified as a collection of solutions
  e.g. may be a list of lists, a numpy array, etc..
  tentatively we return them in the same order as the
  original article with the S heuristic

there a are 3 helper tools that help canocalize solutions for comparison
"""

from importlib import resources

import numpy as np
import pandas as pd

DTYPE_FOR_ARRAY = bool


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


# may be useful to test the algorithm on a trivial problem
# since this is the one illustrated in the original article
def knuth_original_problem():
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


# same problem in fact, but expressed a little differently
# https://en.wikipedia.org/wiki/Exact_cover#Detailed_example
def detailed_wikipedia_problem():
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


def bruteforce_problem1():
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


def bruteforce_problem2():
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


def bruteforce_problem3():
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


def bruteforce3_with_odd_zero_rows_problem():
    p = bruteforce_problem3()
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


def bruteforce3_with_even_zero_rows_problem():
    p = bruteforce_problem3()
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
def small_trimino_problem():
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


def small_trimino_problem_from_file():
    return dict(
        data=np.load("tests/data/small_trimino.npy"),
        solutions=[(5, 13), (6, 12)],
    )


def load_csv(filename):
    with resources.path("exact_cover_samples.data", f"{filename}.csv") as p:
        return pd.read_csv(p, header=None).to_numpy()

def pentomino_chessboard_problem():
    to_cover = load_csv("pentominos-chessboard")
    solutions = load_csv("pentominos-chessboard-solutions")

    return dict(
        data=to_cover,
        solutions=solutions,
    )


def pentomino_5_12_problem():
    to_cover = load_csv("pentominos-5-12")
    solutions = load_csv("pentominos-5-12-solutions")
    return dict(
        data=to_cover,
        solutions=solutions,
    )

# a dictionary
# problem_name -> problem_function
# testers can iterate on this dict to test all problems

ALL_PROBLEMS = {
    symbol: globals()[symbol]
    for symbol in globals() if "_problem" in symbol
}


def summary():
    """
    convenience to display a summary of all problems
    """
    print(f"{8*'-'} we have a total of {len(ALL_PROBLEMS)} problems")
    for name, function in ALL_PROBLEMS.items():
        problem = function()
        data = problem["data"]
        solutions = problem["solutions"]
        print(f"{4*'='} Problem '{name}'")
        print(f"size = {data.shape}, "
              f"{len(canonical(solutions))} solutions")

if __name__ == "__main__":
    summary()
