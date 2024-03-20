# develop and release

## requirements

```bash
pip install .[build]
```

## build

```bash
rm -rf dist/*
python -m build
```

## publish

```bash
twine upload dist/*
```
