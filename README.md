# dcinside-python3-api

Deadly simple non official async dcinside api for python3

## Dependency

- python(>3.6)
- aiohttp
- lxml

## Features

- [x] Board crawling
- [x] Fetch document body
- [x] Fetch comments 
- [x] Fetch document images
- [x] Write/Modify/Delete document
- [x] Write comment
- [ ] Delete comment
- [ ] Login/Logout
- [ ] Upvote/Downvote

## Install

install via pip

```
pip3 install --user dc_api
```

import like this:

```py
import dc_api

api = dc_api.API()

# ...
```

```py
import dc_api

async def main():
  async with dc_api.API() as api:
    # ...
```

## Unit Test

run the following code:

```py
python test_dc_api.py
```

## Issue

very special case where document have empty title: <https://gall.dcinside.com/board/view/?id=programming&no=231191&page=1>
this causes error in `API.document()` method
```
 author = doc_head_container[1][0][0].text.strip()
AttributeError: 'NoneType' object has no attribute 'strip'
```
