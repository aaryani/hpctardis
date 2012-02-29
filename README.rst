
HPCTardis: Data Capture from High-Performance Computing
=======================================================

MyTARDIS is a multi-institutional collaborative venture that
facilitates the archiving and sharing of data and metadata collected
at major facilities such as the Australian Synchrotron and ANSTO and
within Institutions.

HPCTardis is a extension of the MyTARDIS system for the task 
of transferring data and metadata from remote high-performance 
computing facilities, automatic extraction of package-specific 
metadata, curation of experiments for researcher access, and 
publishing of metadata to ANDS.

Documentation
-------------

Installation, User and Developer Manuals are available at http://hpctardis.readthedocs.org


Installation
------------

Get the latest version of myTardis::

  git clone https://github.com/mytardis/mytardis.git

Install and configure mytardis based on instructions at http://mytardis.readthedocs.org/en/latest/install.html
  
Install hpctardis extensions::

  cd mytardis/tardis
  git clone https://github.com/aaryani/hpctardis.git
  
If this worked then the ``hpctardis`` directory should be a the same level as the ``tardis_portal`` directory.

The file ``tardis/test_settings.hpctardis.py.changeme`` is an alternative ``test_settings.py`` for nytardis that includes support for hpctardis extensions

The file ``tardis/settings.hpctardis.py.changeme`` is an example ``settings_changeme.py`` for mytardis that includes support for hpctardis extensions
   
Acknowledgements
----------------

The HPCTardis project includes development funded by the _Australian National Data Service_ (ANDS, http://ands.org.au/ ). ANDS is supported by the Australian Government through the _National Collaborative Research Infrastructure Strategy Program_ and the _Education Investment Fund (EIF) Super Science Initiative_ .


