# PyZenHub

Python bindings to the Zenhub API

## Usage

```python
from zenhub import Zenhub

zh = Zenhub(<zenhub_token>)
zh.get_epics(<repo_id>)
```

For enterprise installs:

```python
from zenhub import Zenhub

zh = Zenhub(<zenhub_token>, base_url=<enterprise-api-endpoint>)
zh.get_epics(<repo_id>)
```

## Documentation

See [ZenHub official API docmuentation](https://github.com/ZenHubIO/API).
