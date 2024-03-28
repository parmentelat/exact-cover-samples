# exact cover samples

contains some exact cover samples together with their solutions.

## installation

```bash
pip install exact-cover-samples
```

## usage

### problems

```python
from exact_cover_samples import problems
```

`problems` is a dictionary with the following structure:

```python
{ "shortname": function, ... }
```

where `shortname` is a string and `function` is a function that in turn returns
a dictionary with the following structure:

```python
{
    "shortname": str,               # short name of the problem
    "name": str,                    # long name of the problem
    "data": np.ndarray,             # of ndim=2 and dtype=bool
    "solutions": list[list[int]]    # each solution is a list of indices in data
}
```

in some cases `solutions` is an nd-array too - see below how to canonicalize for
comparing solutions.

### summary

you can display a summary of the available problems by running the following code:

```python
from exact_cover_samples import summary

summary()
```

will show all known problems
```
# you can also filter a bit
summary("pent")
->
the problems whose name contains 'pent' are:
===================== p3x20 ======================
size = (1236, 72),  8 solutions full_name=pentominos-3-20
===================== p4x15 ======================
size = (1696, 72),  1472 solutions full_name=pentominos-4-15
```

### canonical representation

```python
from exact_cover_samples import problems, canonical

p = problems["knuth2000"]()
s = p["solutions"]
type(s)
-> list
type(s[0])
-> tuple
type(canonical(s))
-> set

p = problems["p8x8"]()
s = p["solutions"]
type(s)
-> numpy.ndarray
type(canonical(s))
-> set
```

so that as long as your code produces solutions as an iterable of iterables,
you should be able to use `canonical` to compare them like so

```
# import this module
import exact_cover_samples as ecs
# import a solver module
from exact_cover_py import exact_covers

# get a problem
p = ecs.problems["knuth2000"]()
# get the expected solutions
expected = p["solutions"]
# get the computed solutions
computed = exact_covers(p["data"])
# compare them
assert ecs.canonical(expected) == ecs.canonical(computed)
```

and so you can write a very decent test suite for your exact cover solver by
simply iterating over the problems in `problems` and comparing the expected
solutions with the computed ones.
