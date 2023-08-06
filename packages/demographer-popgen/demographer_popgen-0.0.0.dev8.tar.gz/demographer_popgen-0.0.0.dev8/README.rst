#DemoGrapher

DemoGrapher is a software tool for drawing and exploring demographic histories.

Quick Start Guide
=================

1. Install DemoGrapher using the `installation instructions`_.
   
2. Launch DemoGrapher by typing ::

     $ demographer

   At a terminal prompt. This command launches the GUI.

3. The commands for DemoGrapher are listed in the output box when
   the program opens. You can also watch the tutorial video at
   the GitHub site.


Installation instructions
=========================

DemoGrapher was developed in Python 2.7 using Enthought Canopy. Check
your Python version at a terminal prompt by typing ::

    $ python --version
    
If you do not have Python 2.7 installed, you can download it. The Anaconda_ 
2 distribution contains all of the packages required for DemoGrapher. However,
any python 2.7 distribution should be fine. If you already have Anaconda_ 3
(which is the Python 3.X release of Anaconda) you can create a Python 2.7
environment using the directions in the `Virtual Environment`_ section below.

Once Python 2.7 (or a virtual environment with Python 2.7) is installed and 
activated, you can install DemoGrapher from the terminal prompt in one of two ways:

1. If you have an Anaconda Python 2.7 release, install using conda ::

    $ conda config --add channels ejewett
    $ conda install demographer
    
   or use ::
   
    $ conda install -n yourenvironmentname demographer
    
   if you are using a `virtual environment`_.

2. If you have a different Python 2.7 release, install using pip ::

    $ pip install demographer_popgen   
    
   or use ::
   
    $ source <path to virtual environment>
    $ pip install demographer_popgen
    
   if you're using a virtual environment

The pip or conda command should download all the necessary files. However, if
you get a "No module named" error, you can individually download the necessary
packages by following the steps in the Troubleshooting_ section.


.. _Anaconda: https://www.continuum.io/downloads


Virtual Environment
-------------------
DemoGrapher installs several dependent packages. Sometimes it is best to
keep these packages within a `virtual environment`_ so that they don't
interfere with the function of other Python software you have installed
and so that updates to other software do not modify the packages that
DemoGrapher relies on. You may also want to use a virtual environment if
you do not have root access to your system or if you're on a shared computer.
You can generate a virtual environment for DemoGrapher in a few ways.

1. If you have an Anaconda Python release (type $ python --version to check)
   you can create a new virtual environment simply by typing ::
   
     $ conda create -n yourchoiceofname python=2.7 anaconda
    
   This creates a new python 2.7 environment named yourchoiceofname
   in your anaconda distribution [1]_. Make the new Python 2.7 
   environment temporarily active by typing ::

     $ source activate yourchoiceofname
   
   (To deactivate yourchoiceofname just type $ deactiveate or open
   a new terminal window). To remove yourchoiceofname entirely type ::
   
     $ conda remove -n yourchoiceofname -all   
     
2. If you are using a Python 2.7 distribution that is not Anaconda,
   you can make a virtual environment using virtualenv. First make 
   sure you have virtualenv installed. To check this, type ::
   
     $ virtualenv --version

   at a command prompt. If a version number appears then it's installed.
   If not, type ::
   
     $ pip install virtualenv
   
   Then type ::

     $ virtualenv <path to a convenient location for your virtual environment directory>
     $ source <path to newly created virtual environment directory>/bin/activate

   For example, if I wanted to put the virtual environment in my user directory
   I would type ::

	 $ virtualenv /Users/ethanjewett/DemoGrapher_venv
	 $ source DemoGrapher_venv/bin/activate

   Once you have executed the source command, install DemoGrapher using
   pip as described above.

.. _virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/


Troubleshooting
-------------------
When installing DemoGrapher with conda or pip, you may find that the packages
you need did not download automatically. For example, you might get the error
"No module named module_name" when running DemoGrapher. If this happens

1. If you are using an Anaconda Python 2.7 distribution (and you are not
   using a virtual environment (see `Virtual Environment`_), type ::

     $ conda install module_name
    
   or ::
   
     $ pip install module_name

   If you are using a virtual environment, type ::

     $ conda install -n yourenvironmentname module_name
     

2. If you are not using Anaconda, type and you are not using a virtual
   environment (see `Virtual Environment`_), type ::
   
     $ pip install module_name
     
   If you are using a virtual environment, first activate the virtual 
   environment by typing ::

     $ source <path to virtual environment>

   Then do ::
   
     $ pip install module_name


.. [1] Unfortunately, creating a virtual environment with conda does not install 
       all of the nice packages that come with Anaconda. So you may have to 
       install them manually if they do not download properly using the
       conda install command in the `Installation Instructions`_ section.
       If you run into an error while installing or trying to run DemoGrapher,
       see Troubleshooting_).