# pymarsys: Python client for the Emarsys API

## pymarsys allows you to choose the type of execution you want for the client: synchronous or asynchronous.

**Warning**: pymarsys is currently under development and on **Pre-Alpha** version. Use with caution!

**Python 2.x compatibility**: If you are using python 2.x, don't, just don't.

### Synchronous example:
```python
    >>> from pymarsys import SyncConnection, Emarsys
    >>> connection = SyncConnection('username', 'secret')
    >>> client = Emarsys(connection)
    >>> client.contacts.create({'3': 'squirrel@squirrelmail.com'})
    {'data': {'id': 19739576}, 'replyCode': 0, 'replyText': 'OK'}
```

### Asynchronous example:
```python
    >>> from pymarsys import AsyncConnection, Emarsys
    >>> async def my_async_func():
    ...     connection = AsyncConnection('username', 'secret')
    ...     client = Emarsys(connection)
    ...     return await client.contacts.create({'3': 'squirrel@squirrelmail.com'})
    >>> my_async_func()
    <coroutine object AsyncConnection.make_call at 0x10c44bd58>
```

#### You will need an event loop to get the result of your coroutine. Here is an example using asyncio's event loop:
```python
    >>> import asyncio
    >>> coroutine = my_async_func()
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(coroutine)
    {'data': {'id': 19739576}, 'replyCode': 0, 'replyText': 'OK'}
```

## Installation

Simply:
```sh
  $ pip install pymarsys
  🐿
```
## Documentation
Coming soon!

##Contributing

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the repository on GitHub to start making your changes.
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published.


