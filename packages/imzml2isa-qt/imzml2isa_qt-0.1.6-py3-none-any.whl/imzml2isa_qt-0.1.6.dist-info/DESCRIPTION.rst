imzml2isa-qt
============

A PyQt interface for mzml2isa parser - imzML edition.
''''''''''''''''''''''''''''''''''''''''''''''''''''''

Overview
--------

This program is a Graphical User Interface for the
`mzml2isa <https://github.com/ISA-tools/mzml2isa>`__ parser. It provides
an easy-to-use interface to convert mzML files to an ISA-Tab Study. It
was made with Python3 and PyQt5.

Install
-------

With PIP
~~~~~~~~

If ``pip`` is present on your system (comes along most of Python install
/ releases), it can be used to install the program and its dependencies:

.. code:: bash

    pip3 install imzml2isa-qt

Without PIP
~~~~~~~~~~~

Once dependencies installed, clone the **imzml2isa-qt** repository to a
folder with writing permissions:

.. code:: bash

    git clone git://github.com/althonos/imzml2isa-qt

After that, either run the GUI directly:

.. code:: bash

    python3 run.py

Or install it locally to run with ``imzmlisa-qt`` command:

.. code:: bash

    cd imzml2isa-qt && python3 setup.py install

Use
---

Open the GUI with the ``imzml2isa-qt`` command. To simply parse **.imzML**
files to **ISA**, select the directory containing your files. With
default settings, the program will create the new ISA files in that
folder, assuming the folder's name is the study identifier (*MTBSLxxx*
for instance for MetaboLights studies). This can be changed by unticking
the ``Export result to directory of each study`` box. Once parameters
are set up, click the ``Convert`` button to start the parser.

MetaboLights
------------

Generating a study to upload on MetaboLights requires pieces of
information the parser cannot guess from the mzML file alone. To provide
more metadata to your final ISA-Tab files, use the ``Add Metadata``
button to open a new window and update details about your study. Still,
even with all the required fields filled, **the generated ISA needs to
be enhanced after the end of the parsing** (using for instance
`Metabolight pre-packaged ISA
Creator <http://www.ebi.ac.uk/metabolights/>`__ to add missing fields).

Missing information required for MetaboLights upload are at the moment:
- Study Factors (sample dependent, must be added to the *study* file
  and to the *investigation* file)
- Metabolite Assignment Files
- Study Designs

TODO
----

-  Either add a ``metabolite assignment file`` field to main window or
   change the **mzml2isa** parser behaviour so that it successfully
   detects metabolite assignment files and add them to the study file.

License
-------

GPLv3


