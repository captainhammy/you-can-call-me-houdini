.. you-can-call-me-houdini documentation master file

Welcome to you-can-call-me-houdini's documentation!
===================================================

``you-can-call-me-houdini`` is a tool that aims to make dealing with Houdini related events easier and
more centralized. Its goal is to handle all the various possible event scripts in one location and allow
easy API access. Client code which wants to be triggered by events should just need to register itself against the
supported events and allow the underlying tooling to handle the invocation and any argument generation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation.rst
   houdini/index.rst
   examples.rst
   api/modules

