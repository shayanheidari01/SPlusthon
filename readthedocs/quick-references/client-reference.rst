.. _client-ref:

================
Client Reference
================

This page contains a summary of all the important methods and properties that
you may need when using SPlusthon. They are sorted by relevance and are not in
alphabetical order.

You should use this page to learn about which methods are available, and
if you need a usage example or further description of the arguments, be
sure to follow the links.

.. contents::

SoroushClient
==============

This is a summary of the methods and
properties you will find at :ref:`splusthon-client`.

Auth
----

.. currentmodule:: splusthon.client.auth.AuthMethods

.. autosummary::
    :nosignatures:

    start
    send_code_request
    sign_in
    qr_login
    log_out
    edit_2fa

Base
----

.. py:currentmodule:: splusthon.client.telegrambaseclient.TelegramBaseClient

.. autosummary::
    :nosignatures:

    connect
    disconnect
    is_connected
    disconnected
    loop
    set_proxy

Messages
--------

.. py:currentmodule:: splusthon.client.messages.MessageMethods

.. autosummary::
    :nosignatures:

    send_message
    edit_message
    delete_messages
    forward_messages
    iter_messages
    get_messages
    pin_message
    unpin_message
    send_read_acknowledge

Uploads
-------

.. py:currentmodule:: splusthon.client.uploads.UploadMethods

.. autosummary::
    :nosignatures:

    send_file
    upload_file

Downloads
---------

.. currentmodule:: splusthon.client.downloads.DownloadMethods

.. autosummary::
    :nosignatures:

    download_media
    download_profile_photo
    download_file
    iter_download

Dialogs
-------

.. py:currentmodule:: splusthon.client.dialogs.DialogMethods

.. autosummary::
    :nosignatures:

    iter_dialogs
    get_dialogs
    edit_folder
    iter_drafts
    get_drafts
    delete_dialog
    conversation

Users
-----

.. py:currentmodule:: splusthon.client.users.UserMethods

.. autosummary::
    :nosignatures:

    get_me
    is_bot
    is_user_authorized
    get_entity
    get_input_entity
    get_peer_id

Chats
-----

.. currentmodule:: splusthon.client.chats.ChatMethods

.. autosummary::
    :nosignatures:

    iter_participants
    get_participants
    kick_participant
    iter_admin_log
    get_admin_log
    iter_profile_photos
    get_profile_photos
    edit_admin
    edit_permissions
    get_permissions
    get_stats
    action

Parse Mode
----------

.. py:currentmodule:: splusthon.client.messageparse.MessageParseMethods

.. autosummary::
    :nosignatures:

    parse_mode

Updates
-------

.. py:currentmodule:: splusthon.client.updates.UpdateMethods

.. autosummary::
    :nosignatures:

    on
    run_until_disconnected
    add_event_handler
    remove_event_handler
    list_event_handlers
    catch_up
    set_receive_updates

Bots
----

.. currentmodule:: splusthon.client.bots.BotMethods

.. autosummary::
    :nosignatures:

    inline_query

Buttons
-------

.. currentmodule:: splusthon.client.buttons.ButtonMethods

.. autosummary::
    :nosignatures:

    build_reply_markup

Account
-------

.. currentmodule:: splusthon.client.account.AccountMethods

.. autosummary::
    :nosignatures:

    takeout
    end_takeout
