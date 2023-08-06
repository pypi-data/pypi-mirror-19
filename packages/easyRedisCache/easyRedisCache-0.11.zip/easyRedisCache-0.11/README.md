# Easy Redis caching decorators

Redis cache implementation for redis caching with multithread/multitask secured thread.

# Requirements

Library was tested in the following environments:

 * Python 2.7, 3.4, 3.5


Feel free to try it in yours, but it's not guaranteed it will work. Submit an issue if you think it should.

# Installation

```
pip install easyRedisCache
```

# Introduction

### Different ways to cache something

```python
# classic way
from easyRedisCache import easyRedisCache

eC = easyRedisCache("keyCache")

import threading
import time

def worker():
    print "Worker 1 Init"
    with eC.setBlocking("key", get=True) as block:
        if block.exception == None:
            #print "Worker 1 Set"
            print block.val
            block.val += "foo"
            time.sleep(1)

def worker2():
    print "Worker 2 Init"
    with eC.setBlocking("key", get=True) as block:
        if block.exception == None:
            #print "Worker 2 Set"
            print block.val
            block.val += "bar"


eC.set("key", "co")

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

for i in range(5):
    t = threading.Thread(target=worker2)
    threads.append(t)
    t.start()

```