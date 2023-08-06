Abstract
========

The 'filesysobjects' package provides utilities for the simplified navigation in filesystem 
hierarchies. 
This comprises advanced search features with the management of multiple
search path lists and 'sys.path', including the mixed application of 're' and 'glob' patterns.

The additional enhancement results in providing OO features on files and
directory trees by enhanced search features,
This comprises patterns and functions on files, directories, and branches.


Blueprint
=========

The 'filesysobjects' package provides utilities for the simplified navigation in filesystem 
hierarchies. 
This comprises basic functions for the application of object oriented patterns 
onto files, directories, and branches.

* **Manage multiple search lists and support 're' and 'glob' for path search**

  Provides the creation and usage of multiple search paths including the
  full scale pattern matching on search paths by 're' and 'glob' `[details] <path_syntax.html#variants-of-pathname-parameters-literals-regexpr-and-glob>`_.

* **Gears for filesystem objects - Files, Directories, and Branches**

  The package provides a set of basic functions for implementing file system items 
  conceptually as classes and objects. Just a few interfaces are required in order to represent 
  some basic OO features on filesystems. This in particular comprises superposition 
  and encapsulation, polymorphism, class and object hierachies.

  * Filesystem elements as classes and objects with multiple search and iteration sets `[details] <path_syntax.html#filesystem-elements-as-objects>`_

  * Standards compliant multiplatform native path support: `[details] <path_syntax.html#syntax-elements>`_ 
    `[examples] <path_syntax_examples.html>`_.

    
  * Programming Interface: 
    `[API] <shortcuts.html#filesysobjects-filesysobjects>`_,
    `[UseCases] <UseCases.html>`_.
      .

* **Yet another attempt for file address processing on network storage**

  Evaluation for an extension modul of the interface 'os.path.normpath'.
  Thus the function is named for now 'filesysobjects.NetFiles.normpathX'.

  * `Extended Filesystems - Network Features <path_netfiles.html>`_
      .

* **RTTI for native Python source files** 

  see
  `PySourceInfo @ https://pypi.python.org/pypi/pysourceinfo <https://pypi.python.org/pypi/pysourceinfo>`_

Fur further information on concepts and workflows refer to:

* Filesystem Elements as Objects
  `[details] <path_syntax.html#filesystem-elements-as-objects>`_

* Variants of Pathname Parameters - Literals, RegExpr, and Glob 
  `[details] <path_syntax.html#variants-of-pathname-parameters-literals-regexpr-and-glob>`_

* Syntax Elements 
  `[details] <path_syntax.html#syntax-elements>`_

* Call Parameters of the API 
  `[details] <path_syntax.html#call-parameters-of-the-api>`_

See the API and subdocument collection in section 
:ref:`'Shortcuts' <shortcs>`
 
Install - HowTo - FAQ - Help
============================

* **Install**:

  Standard procedure online local install by sources::

    python setup.py install --user

  Custom procedure offline by::

    python setup.py install --user --offline

  Documents, requires Sphinx and Epydoc::

    python setup.py build_doc install_doc

* **Introduction**:

  For now refer to the listed API and subdocument collection in section 
  :ref:`'Shortcuts' <shortcs>`


`Shortcuts <shortcuts.html>`_
=============================

.. _shortcs:

Concepts and workflows:

* Filesystem Elements as Objects
  `[details] <path_syntax.html#filesystem-elements-as-objects>`_

* Variants of Pathname Parameters - Literals, RegExpr, and Glob 
  `[details] <path_syntax.html#variants-of-pathname-parameters-literals-regexpr-and-glob>`_

* Syntax Elements 
  `[details] <path_syntax.html#syntax-elements>`_

* Call Parameters of the API 
  `[details] <path_syntax.html#call-parameters-of-the-api>`_

Common Interfaces:

* `Programming Interface <shortcuts.html>`_

* `Selected Common UsesCases <usecases.html>`_

Complete technical API:

* Interface in javadoc-style `[API] <epydoc/index.html>`_


Table of Contents
=================
   
 
.. toctree::
   :maxdepth: 3

   shortcuts
   usecases
   filesysobjects
   netfiles
   UseCases
   tests
   testdata

* setup.py

  For help on extensions to standard options call onlinehelp:: 

    python setup.py --help-filesysobjects



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Resources
=========

For available downloads refer to:

* Python Package Index: https://pypi.python.org/pypi/pyfilesysobjects

* Sourceforge.net: https://sourceforge.net/projects/filesysobjects/

* github.com: https://github.com/ArnoCan/filesysobjects/

For Licenses refer to enclosed documents:

* Artistic-License-2.0(base license): `ArtisticLicense20.html <_static/ArtisticLicense20.html>`_

* Forced-Fairplay-Constraints(amendments): `licenses-amendments.txt <_static/licenses-amendments.txt>`_ / `Protect OpenSource Authors <http://xkcd.com/1303/>`_

