# Contributing to this repository

## Clone

To get started fork this repository, and clone your fork:

```bash
# clone your fork
git clone https://github.com/<your_organization>/pyzenhub
cd pyzenhub

# install pre-commit hooks
pre-commit install

# install in editable mode
pip install -e .

# run tests & make sure everything is working!
pytest tests --cov=zenhub --cov-report term-missing
```
