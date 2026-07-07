SPlusthon
=========

**SPlusthon** is an asyncio Python 3 MTProto library to interact with
`Soroush Plus <https://web.splus.ir>`_'s API as a user or through a
bot account (bot API alternative).

SPlusthon is a fork of Telethon adapted to work with the Soroush Plus
messenger. It uses Soroush-specific TL schema (layer 182), DC routing,
RSA keys, and WebSocket transport.

.. note::

    As with any third-party library for Soroush Plus, be careful not to
    break Soroush Plus's Terms of Service or risk an account ban.

What is this?
-------------

Soroush Plus is a popular messaging application. This library is meant
to make it easy for you to write Python programs that can interact
with Soroush Plus. Think of it as a wrapper that has already done the
heavy job for you, so you can focus on developing an application.


Installing
----------

.. code-block:: sh

  pip3 install splusthon


Creating a client
-----------------

SPlusthon includes default API credentials for Soroush Plus, so you
can create a client without obtaining your own keys:

.. code-block:: python

    from splusthon import SoroushClient, events, sync
    from splusthon.sessions import StringSession

    # No api_id or api_hash needed - defaults are included
    client = SoroushClient(StringSession(), session_string=None)
    client.start()


Doing stuff
-----------

.. code-block:: python

    print(client.get_me().stringify())

    client.send_message('username', 'Hello! Talking to you from SPlusthon')
    client.send_file('username', '/home/myself/Pictures/holidays.jpg')

    client.download_profile_photo('me')
    messages = client.get_messages('username')
    messages[0].download_media()

    @client.on(events.NewMessage(pattern='(?i)hi|hello'))
    async def handler(event):
        await event.respond('Hey!')


Using an existing session
-------------------------

If you have a saved session string, you can restore it:

.. code-block:: python

    from splusthon import SoroushClient
    from splusthon.sessions import StringSession

    session_string = '1AwA...'  # from a previous run
    with SoroushClient(StringSession(session_string)) as client:
        print(client.get_me())


Links
-----

- GitHub: https://github.com/shayanheidari01/SPlusthon
- Soroush Plus: https://web.splus.ir
