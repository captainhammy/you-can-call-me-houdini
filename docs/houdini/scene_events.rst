============
Scene Events
============

Please see the `documentation <https://www.sidefx.com/docs/houdini/hom/locations.html#run-scripts-before-and-or-after-saving-the-scene-hip-file>`_
for a description on the specific scripts.

afterscenesave.py
-----------------

The ``afterscenesave.py`` script will emit the :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniSessionEvent.AfterSceneSave` event.


beforescenesave.py
------------------

The ``beforescenesave.py`` script will emit the :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniSessionEvent.BeforeSceneSave` event.

