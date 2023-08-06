trabBuild
=========

Update package version, build, and upload to PyPi. All in one step!


Install
-------

trabBuild is available on PyPi. ::

    pip install trabBuild

Or install directly from setup.py ::

    python setup.py install


Usage
-----

Navigate to the directory with the package and setup.py file you want to update and build, then type. ::

    $ trabbuild

trabBuild will first update the version number in your setup.py file
based on your input, then call `python setup.py sdist` and `python
setup.py bdist_wheel --universal` to build your package.

Once built you will be given the option to upload your package to
PyPi with `twine`. *NOTE: You must already have an account on PyPi for this part to work.*

***NOTE***
**Package version must be specified in setup.py with this format** ::

    __version__ = "x.x.x"


Sample
------

.. image:: trabBuild.png
    :align: center
    :alt: alternate text
