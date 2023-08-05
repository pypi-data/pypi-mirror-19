# FALSY

```
name: FAL.S.Y
version: 2017.01.02
summary: falcon.swagger.yaml
author: Jesse MENG (dameng/pingf)
author-email: pingf0@gmail.com

Intended Audience: Web Developers
License: Apache Software License
License: MIT License
Programming Language: Python3
```

```python
    from falsy.falsy import FALSY

    f = FALSY(static_path='test', static_dir='static')
    f.begin_api()
    f.swagger('test.yml', ui=True,theme='impress')
    f.end_api()
    api = f.api
```



