# PyZenHub

Python bindings to the Zenhub API.

## Project status

[![License](https://img.shields.io/pypi/l/pyzenhub.svg?color=green)](https://github.com/goanpeca/pyzenhub/raw/main/LICENSE.txt)
[![PyPI](https://img.shields.io/pypi/v/pyzenhub.svg?color=green)](https://pypi.org/project/pyzenhub)
[![Python
Version](https://img.shields.io/pypi/pyversions/pyzenhub.svg?color=green)](https://python.org)
[![Tests](https://github.com/goanpeca/pyzenhub/actions/workflows/test_pull_request.yml/badge.svg?branch=main)](https://github.com/goanpeca/pyzenhub/actions/workflows/test_pull_request.yml)
[![Typing](https://github.com/goanpeca/pyzenhub/actions/workflows/test_typing.yml/badge.svg)](https://github.com/goanpeca/pyzenhub/actions/workflows/test_typing.yml)
[![codecov](https://codecov.io/gh/goanpeca/pyzenhub/branch/main/graph/badge.svg?token=dcsjgl1sOi)](https://codecov.io/gh/goanpeca/pyzenhub)

## Usage

```python
from zenhub import Zenhub

zh = Zenhub('<zenhub_token>')
zh.get_epics('<repo_id>')  # Dictionary
```

Return models instead of dictionaries

```python
from zenhub import Zenhub

zh = Zenhub('<zenhub_token>', return_models=True)
zh.get_epics('<repo_id>')  # Pydantic model!
```

*Methods will always return dates as `datetime.datetime` objects, not strings.*

### For enterprise installs

```python
from zenhub import Zenhub

zh = Zenhub('<zenhub_token>', base_url='<enterprise-api-endpoint>')
zh.get_epics('<repo_id>')
```

To select the enterprise version use the `enterprise` parameter.

```python
from zenhub import Zenhub

zh2 = Zenhub('<zenhub_token>', base_url='<enterprise-api-endpoint>', enterprise=2)
zh.get_epics('<repo_id>')

zh3 = Zenhub('<zenhub_token>', base_url='<enterprise-api-endpoint>', enterprise=3)
zh.get_epics('<repo_id>')
```

## Documentation

See [ZenHub official API documentation](https://github.com/ZenHubIO/API).
