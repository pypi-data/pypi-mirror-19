Pydata project
==============

Python project, which also includes command line interface using click (optional).

Its simple structure contains only the project directory a main script
and the main function. Additionally, it also comes with a simple :file:`setup.py` script,
a :file:`README.rst` file and a :file:`LICENSE.txt`.


Structure
---------

::

   project/
   |
   |-- project/
   |   |-- __init__.py
   |   |-- main.py
   |
   |-- LICENSE.txt
   |-- README.rst
   |-- setup.py


Additional features
-------------------

Command line interface (CLI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The project can include some minimal code to enable the use of the package from the command line.
The command line interface is done using `click <http://click.pocoo.org>`_.


Conda environment
^^^^^^^^^^^^^^^^^

The build process will also suggest the creation of a conda environment.
If it is accepted, the project will also be installed in the new environment in
developer mode.


Version control
^^^^^^^^^^^^^^^

Finally, the option to start a git repository and to connect it to a remote
is also provided.
