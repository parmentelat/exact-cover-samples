# publish

```bash
# install build dependencies
pip install .[build]

# clean up former builds
rm -rf dist/*

# build in dist/
python -m build

# publish on pypi
twine upload dist/*
```
