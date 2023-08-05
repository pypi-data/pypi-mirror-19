Pybrood
=======

|docs|

Binding made as from-scratch code generator, outputting msvc project.

Requirements
------------

-  Windows 7 32 bit (just exactly SSCAIT requirement)
    NOTE: I couldn't successfully run BWAPI injector under Wine,
   although recently I've been told
    `it's
   possible <https://github.com/TorchCraft/TorchCraft/blob/master/docs/user/bwapi_on_linux.md>`__.
-  `Python
   3.5 <https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe>`__
-  `Visual C++ build
   tools <http://landinghub.visualstudio.com/visual-cpp-build-tools>`__
   or complete Visual Studio.
    NOTE: pick the version of compiler/studio considering `build tools
   used by python <https://wiki.python.org/moin/WindowsCompilers>`__
-  `BWAPI 4.1.2
   sources <https://github.com/bwapi/bwapi/releases/tag/v4.1.2>`__
    you need ``BWAPI.lib`` and ``BWAPIClient.lib`` built against chosen
   compiler to link pybrood module
-  Most fresh (dec 2016) `Pybind11
   headers <https://github.com/pybind/pybind11>`__

Building BWAPI.lib and BWAPIClient.lib
--------------------------------------

| You may experience "access denied" errors while working directly in
  "program files/BWAPI".
| Better use separately cloned git repo of BWAPI where you have full
  access.

| For ``msbuild`` invocation use special VC++ related cmd shell from
  Launch menu.
| Otherwise you can use usual cmd shell.

#. Make some changes in bwapi source files first:

-  | little fix in ``bwapi/include/BWAPI/SetContainer.h:54``:
   |  at very end of class add

   ``SetContainer& operator=(const SetContainer&) = default;``

   to get rid of "attempting to reference a deleted function" error.

-  disable mass file copying in ``bwapi/BWAPILIB/BWAPILIB.vcxproj``:

   -  line 64: ``<PreLinkEvent>`` â†’ ``<!-- PreLinkEvent>``

      -  line 94: ``</PreLinkEvent>`` â†’ ``</PreLinkEvent -->``

-  create file ``bwapi/svnrev.h``:

   ``static const int SVN_REV = 4708;  #include "starcraftver.h"``

   This prevents "Client and Server are not compatible" error.

#. Build BWAPI.lib:

``cd bwapi\BWAPILIB\    msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32``

Output file is ``bwapi/lib/BWAPI.lib``.

#. Build BWAPIClient.lib:

``cd bwapi\BWAPIClient\    msbuild /p:PlatformToolset=v140 /p:Configuration=Release /p:Platform=Win32``

Output file is ``bwapi/lib/BWAPIClient.lib``.

Building Pybrood
----------------

#. Setup paths in `config.py <generator/config.py>`__.
#. Run the generator ``python3.5 -m generator``.
#. ``cd`` to freshly generated ``output`` folder and run ``build.bat``
   (it's just the same msbuild command).
#. Copy/symlink ``output/Release/inner.pyd`` into ``pybrood`` directory.
    ``inner.pyd`` is a required submodule of ``pybrood``.
#. Now you should be able to ``import pybrood``.

Documentation
-------------

`Read the docs <http://pybrood.readthedocs.io/en/latest/>`__

You can also build your local copy of documentation after running the
generator:

::

    cd output/docs/
    sphinx-build . -b html _build/html

.. |docs| image:: https://readthedocs.org/projects/pybrood/badge/?version=latest
   :target: http://pybrood.readthedocs.io/en/latest/


