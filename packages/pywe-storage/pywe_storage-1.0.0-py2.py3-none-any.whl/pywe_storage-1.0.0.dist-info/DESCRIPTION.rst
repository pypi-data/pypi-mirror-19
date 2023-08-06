============
pywe-storage
============

Wechat Storage Module for Python.

Installation
============

::

    pip install pywe-storage


Usage
=====

MemoryStorage::

    In [1]: from pywe_storage import MemoryStorage

    In [2]: storage = MemoryStorage()

    In [3]: storage.set('xx:oo', {'a': 1, 'b': 2})

    In [4]: storage.get('xx:oo')
    Out[4]: {'a': 1, 'b': 2}


RedisStorage::

    In [1]: import redis_extensions as redis

    In [2]: r = redis.StrictRedisExtensions(host='localhost', port=6379, db=0)

    In [3]: from pywe_storage import RedisStorage

    In [4]: storage = RedisStorage(r)

    In [5]: storage.set('xx:oo', {'a': 1, 'b': 2})

    In [6]: storage.get('xx:oo')
    Out[6]: {u'a': 1, u'b': 2}

    In [7]: r.get('pywe:xx:oo')
    Out[7]: '{"a": 1, "b": 2}'


Method
======

::

    class MemoryStorage(BaseStorage):
        def __init__(self, prefix='pywe'):

    class RedisStorage(BaseStorage):
        def __init__(self, redis, prefix='pywe'):



