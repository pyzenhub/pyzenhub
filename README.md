# PyZenHub

Python bindings to the Zenhub API.

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

To select the enterprise version use the `enterprise` parameter. 

```python
from zenhub import Zenhub

zh2 = Zenhub(<zenhub_token>, base_url=<enterprise-api-endpoint>, enterprise=2)
zh.get_epics(<repo_id>)

zh3 = Zenhub(<zenhub_token>, base_url=<enterprise-api-endpoint>, enterprise=3)
zh.get_epics(<repo_id>)
```

## Documentation

See [ZenHub official API documentation](https://github.com/ZenHubIO/API).
