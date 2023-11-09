Directory content.
==================

This directory contains the development of an application called **SyncMeasures** 
which reorganizes sets of measures into a table of synchronized readings. The sets
of measures are first presented one below each other. Each set start by the name of 
the measures follow by couple, each presented on one line, first item being the time
of the reading and the second the value. Each sets are moved in front of each other
and then merge into a table with a common time scale.

.. image:: img/settable.png
    :width: 762
    :align: center
    :alt: sets into a table

In order to test this application, a second application is also developed, called
**GenSets**, which propose to generates sets of fictive measures for testing the
first application.

Both application are developed under **Python** and with **tkInter**. The development
is fully documented with **Sphinx**.


Directory organization.
=======================

The **SyncMeasures** application main file is `syncreadings.py` on the root directory.
It is the file to be launched to run the applicaiton. It is using libraries placed in 
the subdirectory `./lib/`. The main file is building the user interface using **tkinter**.  
The main file in the library is `./lib/transform_sets.py`, which contains the main 
functions manipulating the data sets. A window showing user instructions is also using 
the *html* files and images stored under the directory `./lib/html`. There is a secondary 
library called `./lib/my_dialogs.py` for building additional dialogs windows, there were 
not available as standard ones.

Some other directories are diving additional resources, as detailed below.

.. list-table:: 
    :widths: 25 75
    :header-rows: 1

    * - Directories
      - Content
    * - `/`
      - Main file, readme, makefile for doc.
    * - `/lib`
      - libraries for the application.
    * - `/lib/html`
      - The html file giving the user instructions.
    * - `/test`
      - scripts used for testing the application.
    * - `/dat`
      - data files used for demonstration.
    * - `/doc`
      - source file for the application documentation.
    * - `/build`
      - documentation automatically generated (sphinx).
    * - `/utils`
      - scripts for supporting distributions and others
    * - `/sandbox`
      - various side tests, not included with the application.
    * - `/trash`
      - garbage, that were not yet totally discarded.
    * - `/.venv`
      - Virtual environmental files from Poetry.
    * - `/vscode`
      - Settings for using Visual Studio Code
  

A development using Poetry.
===========================

My personal installation of Python is using official Ubuntu repositories 
installed with `apt`. This means, I cannot install the libraries not
forecasted by *Debian* team, which is quite conservative. As example, the
library `esbonio`_, which allows to have previews of **RST** files within 
a **Sphinx** project is not available. For this reason, I choose anyhow to 
work with a virtual environment, which release me from such constraints.

.. _esbonio: <https://github.com/swyddfa/esbonio>

I have chosen `Poetry <https://python-poetry.org/>`_ as virtual environment.
It installs its files under the directory `/.venv`. This directory can be
discarded with its content. What is important to record for this virtual
environment is stored in the file `pyproject.toml`, which is at the root of
this directories. This file is storing the general information on the
project, the version of Python that should be used for it and the libraries
that are used for it.

Here is the content of this file.
	    
.. literalinclude:: ../pyproject.toml
   :language: toml
   :caption: Settings of Poetry with pyproject.toml
   

Working with Visual Studio Code.
================================
	     
To work easily with Visual Studio Code (**VSC**), some settings are defined
in `/.vscode/settings.json`. It allows in particular to use the Python
debugger on any Python script.

.. literalinclude:: ../.vscode/settings.json
   :language: json
   :caption: Settings for using under VSC.

The library `esbonio`_ and `pip`_ have been added to virtual environment. It allows 
to install further python extensions. Those were required to install the `esbonio_add-ins`_
and `RST Preview`_ which allows to have a pre-visualisation of the RST files.

.. _pip: https://pip.pypa.io/en/stable/index.html
.. _esbonio_add-ins: https://marketplace.visualstudio.com/items?itemName=swyddfa.esbonio
.. _RST preview: https://marketplace.visualstudio.com/items?itemName=tht13.rst-vscode


Working with Emacs.
===================

For Emacs, one can install through **elpa** repositories *sphinx-mode* and *sphinx-doc*.



