# PyZenHub

Python bindings to the Zenhub API

## Usage

```python
from zenhub import ZenHub

zh = ZenHub(<zenhub_token>)
zh.get_epics(<repo_id>)
```
