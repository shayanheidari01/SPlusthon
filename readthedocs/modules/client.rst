.. _splusthon-client:

==============
SoroushClient
==============

.. currentmodule:: splusthon.client

The `SoroushClient <telegramclient.SoroushClient>` aggregates several mixin
classes to provide all the common functionality in a nice, Pythonic interface.
Each mixin has its own methods, which you all can use.

**In short, to create a client you must run:**

.. code-block:: python

    from splusthon import SoroushClient

    client = SoroushClient(name, api_id, api_hash)

    async def main():
        # Now you can use all client methods listed below, like for example...
        await client.send_message('me', 'Hello to myself!')

    with client:
        client.loop.run_until_complete(main())


You **don't** need to import these `AuthMethods`, `MessageMethods`, etc.
Together they are the `SoroushClient <telegramclient.SoroushClient>` and
you can access all of their methods.

See :ref:`client-ref` for a short summary.

.. automodule:: splusthon.client.soroushclient
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.telegrambaseclient
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.account
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.auth
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.bots
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.buttons
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.chats
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.dialogs
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.downloads
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.messageparse
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.messages
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.updates
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.uploads
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: splusthon.client.users
    :members:
    :undoc-members:
    :show-inheritance:
