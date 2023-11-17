=======================
Supported Houdini Items
=======================

Unfortunately Houdini has a variety of ways in which it can respond to various types of events. While some of the
more recent ones are explicitly defined Python callbacks, most of the handling is done by legacy disk-based event
scripts. Adding to the confusion, these files can be placed in multiple places and also work to override default
versions shipped with Houdini itself.  Below you'll find a description of the various event types that ``you-can-call-me-houdini``
supports.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   event_handlers
   scene_events
   startup_scripts
   other
   default_callbacks
