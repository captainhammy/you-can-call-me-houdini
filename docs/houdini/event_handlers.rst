===================
Node Event Handlers
===================

Please see the `documentation <https://www.sidefx.com/docs/houdini/hom/locations.html#asset_events>`_ for descriptions
of the specific event handler scripts.

Available Events / Scripts
--------------------------

All the known event handling scripts (OnCreated.py, OnLoaded.py, etc.) are provided and each will emit a correspondingly
named :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeEvent` event.

.. list-table::
    :header-rows: 1

    * - Event Script
      - Enum

    * - **OnCreated.py**
      - :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeEvent.OnCreated`
    * - **OnLoaded.py**
      - :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeEvent.OnLoaded`
    * - **etc.**
      - ...

These events are emitted with the Houdini provided ``kwargs`` passed along.

Most Scripts Disabled By Default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most scripts are disabled by default (by way of adding an '_' to their name (eg. _OnLoaded.py) for performance reasons. As
many of these scripts can be run by Houdini a massive number of times this can cause adverse effects and it is recommended
that you only enable ones that you need.

To enable specific scripts, remove the leading '_' in the file names located under the ``houdini/scripts`` directory.

Default Scripts
---------------

By default, the following event handler scripts are enabled:

    - OnCreated.py
    - OnInstall.py
    - OnNameChanged.py
    - OnUninstall.py
