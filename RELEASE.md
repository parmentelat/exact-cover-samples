# develop and release

## build

```bash
rm -rf dist/*
python -m build
```

## publish

```bash
twine upload dist/*
```
