# Release

```bash
git tag -a vX.X.X -m 'Release version vX.X.X'
```

```bash
python -m build
twine check dist/*
twine upload dist/*
```
