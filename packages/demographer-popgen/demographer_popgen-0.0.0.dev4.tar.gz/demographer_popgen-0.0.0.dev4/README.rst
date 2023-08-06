DemoGrapher is a software tool for drawing and exploring demographic histories.

Quick Start Guide
=================

1. Install DemoGrapher using the `installation instructions`_.
   
2. Launch DemoGrapher by typing ::

     $ demographer

   At a terminal prompt. This command launches the GUI.

3. The commands for DemoGrapher are listed in the output box when
   the program opens. You can also watch the tutorial video that
   can be downloaded from the GitHub site.


Installation instructions
=========================

DemoGrapher was developed in Python 2.7 using Enthought Canopy. Check
your Python version at a terminal prompt by typing ::

    $ python --version
    
If you do not have Python 2.7 installed, you can download either the
`Enthought Canopy`_ or Anaconda_ distribution. Once Python 2.7 is 
installed on your machine, you can install DemoGrapher from a terminal 
prompt using pip ::

    $ pip install demographer_popgen

The pip command will download all the necessary files.

.. _Enthought Canopy: https://www.enthought.com/products/canopy/
.. _Anaconda: https://www.continuum.io/downloads


Virtual Environment
-------------------
DemoGrapher installs several dependent packages. Sometimes it is best to
keep these packages within a `virtual environment`_ so that they don't
interfere with the function of other Python software you have installed
and so that updates to other software do not modify the packages that
DemoGrapher relies on. You may also want to use a virtual environment if
you do not have root access to your system. To generate a virtual
environment for DemoGrapher, first make sure you have virtualenv installed.
To check, type 

	$ virtualenv --version

at a command prompt. If a version number appears then it's installed.
Some open a terminal prompt and type::

    $ virtualenv <path to a convenient location for your virtual environment directory>
    $ source <newly created virtual environment directory>/bin/activate

For example, if I want to put the virtual environment in my user directory
I would personally type

	$ virtualenv /Users/ethan/DemoGrapher_venv
	$ source DemoGrapher_venv/bin/activate

Once you have executed the source command, install DemoGrapher using
pip as described above.

.. _virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/

