API Shortcuts - filesysobjects
==============================

The applicable match scope for a filepathname input is displayed
in the column `[scope] <path_syntax.html#variants-of-pathname-parameters-literals-regexpr-and-glob>`_.

The search path list is supported as literal only.

* L,l: literal

* R,r: regexpr by 're'

* G,g: 'glob'

The case of the characters for resolution '[scope]' indicate their handling:
 
* upper case - L, R, G - Upper case letters indicate active resolution including in-memory processing and filesystem access.

* lower case - l, r, g - Lower case letters indicate passive string acceptance with some in-memory processing.

The column '[fs]' displays whether the filesystem is accessed, or in mem file search paths only.
Function calls which access the filesystem are marked in the column '[fs]' with 'X'.

filesysobjects.FileSysObjects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Filesystem Positions and Navigation for *sys.path*, and extended alternatives.
`[docs] <filesysobjects.html#>`_

* manage search paths - checks filesystem

  +---------------------------------+----------------------------------------------------+---------+------+
  | [docs]                          | [source]                                           | [scope] | [fs] |
  +=================================+====================================================+=========+======+
  | `addPathToSearchPath`_          | `FileSysObjects.addPathToSearchPath`_              | L       | X    |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `clearPath`_                    | `FileSysObjects.clearPath`_                        | L       | X    |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `delPathFromSearchPath`_        | `FileSysObjects.delPathFromSearchPath`_            | LRG     | X    |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `setUpperTreeSearchPath`_       | `FileSysObjects.setUpperTreeSearchPath`_           | L       | X    |
  +---------------------------------+----------------------------------------------------+---------+------+

.. _FileSysObjects.addPathToSearchPath: _modules/filesysobjects/FileSysObjects.html#addPathToSearchPath
.. _FileSysObjects.delPathFromSearchPath: _modules/filesysobjects/FileSysObjects.html#delPathFromSearchPath
.. _FileSysObjects.clearPath: _modules/filesysobjects/FileSysObjects.html#clearPath
.. _FileSysObjects.setUpperTreeSearchPath: _modules/filesysobjects/FileSysObjects.html#setUpperTreeSearchPath

.. _addPathToSearchPath: filesysobjects.html#addpathtosearchpath
.. _clearPath: filesysobjects.html#clearpath
.. _delPathFromSearchPath: filesysobjects.html#delpathfromsearchpath
.. _setUpperTreeSearchPath: filesysobjects.html#setuppertreesearchpath


* search for appended paths of files, directories, and branches - check filesystem

  +---------------------------------+----------------------------------------------------+---------+------+
  | [docs]                          | [source]                                           | [scope] | [fs] |
  +=================================+====================================================+=========+======+
  | `findRelPathInSearchPath`_      | `FileSysObjects.findRelPathInSearchPath`_          | LG      | X    |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `findRelPathInSearchPathIter`_  | `FileSysObjects.findRelPathInSearchPathIter`_      | LG      | X    |
  +---------------------------------+----------------------------------------------------+---------+------+

.. _FileSysObjects.findRelPathInSearchPath: _modules/filesysobjects/FileSysObjects.html#findRelPathInSearchPath
.. _FileSysObjects.findRelPathInSearchPathIter: _modules/filesysobjects/FileSysObjects.html#findRelPathInSearchPathIter

.. _findRelPathInSearchPath: filesysobjects.html#findrelpathinsearchpath
.. _findRelPathInSearchPathIter: filesysobjects.html#findrelpathinsearchpathiter

* match files, directories, and branches into path strings - work on strings only

  +---------------------------------+----------------------------------------------------+---------+------+
  | [docs]                          | [source]                                           | [scope] | [fs] | 
  +=================================+====================================================+=========+======+
  | `getTopFromPathString`_         | `FileSysObjects.getTopFromPathString`_             | LRg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `getTopFromPathStringIter`_     | `FileSysObjects.getTopFromPathStringIter`_         | LRg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+

.. _FileSysObjects.getTopFromPathString: _modules/filesysobjects/FileSysObjects.html#getTopFromPathString
.. _FileSysObjects.getTopFromPathStringIter: _modules/filesysobjects/FileSysObjects.html#getTopFromPathStringIter

.. _getTopFromPathString: filesysobjects.html#gettopfrompathstring
.. _getTopFromPathStringIter: filesysobjects.html#gettopfrompathstringiter

* canonical user data hooks - provide major context directories for os.platform

  +---------------------------------+----------------------------------------------------+---------+------+
  | [docs]                          | [source]                                           | [scope] | [fs] | 
  +=================================+====================================================+=========+======+
  | `getHome`_                      | `FileSysObjects.getHome`_                          | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `getDirUserData`_               | `FileSysObjects.getDirUserData`_                   | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `getDirUserConfigData`_         | `FileSysObjects.getDirUserConfigData`_             | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `getDirUserAppData`_            | `FileSysObjects.getDirUserAppData`_                | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+

.. _FileSysObjects.getHome: _modules/filesysobjects/FileSysObjects.html#getHome
.. _getHome: filesysobjects.html#gethome

.. _FileSysObjects.getDirUserData: _modules/filesysobjects/FileSysObjects.html#getDirUserData
.. _getDirUserData: filesysobjects.html#getdiruserdata

.. _FileSysObjects.getDirUserConfigData: _modules/filesysobjects/FileSysObjects.html#getDirUserConfigData
.. _getDirUserConfigData: filesysobjects.html#getdiruserconfigdata

.. _FileSysObjects.getDirUserAppData: _modules/filesysobjects/FileSysObjects.html#getDirUserAppData
.. _getDirUserAppData: filesysobjects.html#getdiruserappdata

Canonical Node Address
^^^^^^^^^^^^^^^^^^^^^^

* Manage pathnames - files, directories, and branches

  +---------------------------------+----------------------------------------------------+---------+------+
  | [docs]                          | [source]                                           | [scope] | [fs] |
  +=================================+====================================================+=========+======+
  | `escapeFilePath`_               | `FileSysObjects.escapeFilePath`_                   | lg      | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `getAppPrefixLocalPath`_        | `FileSysObjects.getAppPrefixLocalPath`_            | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `normpathX`_                    | `FileSysObjects.normpathX`_                        | l       | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `splitAppPrefix`_               | `FileSysObjects.splitAppPrefix`_                   | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `splitPathVar`_                 | `FileSysObjects.splitPathVar`_                     | lrg     | --   |
  +---------------------------------+----------------------------------------------------+---------+------+
  | `unescapeFilePath`_             | `FileSysObjects.unescapeFilePath`_                 | lg      | --   |
  +---------------------------------+----------------------------------------------------+---------+------+

.. _FileSysObjects.escapeFilePath: _modules/filesysobjects/FileSysObjects.html#escapeFilePath
.. _FileSysObjects.getAppPrefixLocalPath: _modules/filesysobjects/FileSysObjects.html#getAppPrefixLocalPath
.. _FileSysObjects.normpathX: _modules/filesysobjects/FileSysObjects.html#normpathX
.. _FileSysObjects.splitAppPrefix: _modules/filesysobjects/FileSysObjects.html#splitAppPrefix
.. _FileSysObjects.splitPathVar: _modules/filesysobjects/FileSysObjects.html#splitPathVar
.. _FileSysObjects.unescapeFilePath: _modules/filesysobjects/FileSysObjects.html#unescapeFilePath

.. _escapeFilePath: filesysobjects.html#escapefilepath
.. _getAppPrefixLocalPath: filesysobjects.html#getappprefixlocalpath
.. _normpathX: filesysobjects.html#normpathx
.. _splitAppPrefix: filesysobjects.html#splitappprefix
.. _splitPathVar: filesysobjects.html#splitpathvar
.. _unescapeFilePath: filesysobjects.html#unescapefilepath


* For now experimental and non-productive, for review and comments
  `[docs] <netfiles.html#>`_

  +---------------------------------+-------------------------------------------------+---------+------+
  | [docs]                          | [source]                                        | [scope] | [fs] |
  +=================================+=================================================+=========+======+
  | `netNormpathX`_                 | `NetFiles.netNormpathX`_                        |         |      |
  +---------------------------------+-------------------------------------------------+---------+------+

.. _netNormpathX: netfiles.html#filesysobjects.NetFiles.netNormpathX
.. _NetFiles.netNormpathX: _modules/filesysobjects/NetFiles.html#netnormpathx



