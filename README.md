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

where `shortname` is a string and `function` is a function that in turn returns a dictionary with the following structure:

```python
{
    "shortname": str,               # short name of the problem
    "name": str,                    # long name of the problem
    "data": np.ndarray,             # of ndim=2 and dtype=bool
    "solutions": list[list[int]]    # each solution is a list of indices in data
}

in some cases `solutions` is an nd-array too - see below how to canonicalize for comparing solutions.
```

### summary

you can display a summary of the available problems by running the following code:

```python
from exact_cover_samples import summary

summary()
# or to filter a bit
summary("pent")
```

### canonical representation

```python
p = problems["knuth-original"]()
s = p["solutions"]
type(s)
-> list
type(s[0])
-> tuple
type(canonical(s))
-> set

p = problems["pentomino-chessboard"]()
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
p = ecs.problems["knuth"]()
# get the expected solutions
expected = p["solutions"]
# get the computed solutions
computed = exact_covers(p["data"])
# compare them
assert ecs.canonical(expected) == ecs.canonical(computed)
```
