UseCase-Shortcuts - Selected Common UsesCases
=============================================

For a complete list refer to `[UseCases] <UseCases.html>`_.

Manage Search Paths
^^^^^^^^^^^^^^^^^^^

  +-----------------------------------------------+--------------------------------------+
  | UseCase                                       | [doc/source]                         | 
  +===============================================+======================================+
  | Create and use a search lists                 | `createAndUseSearchLists`_           |
  +-----------------------------------------------+--------------------------------------+
  | Create and use a search lists from glob       | `createAndUseSearchListsFromGlob`_   |
  +-----------------------------------------------+--------------------------------------+
  | Add and remove entries                        | `addAndRemoveEntries`_               |
  +-----------------------------------------------+--------------------------------------+
  | Normalize search path lists                   | `normalizeSearchPathLists`_          |
  +-----------------------------------------------+--------------------------------------+

.. _createAndUseSearchLists: UseCases.FileSysObjects.createAndUseSearchLists.from_literal.html#
.. _createAndUseSearchListsFromGlob: UseCases.FileSysObjects.createAndUseSearchLists.from_glob.html#
.. _addAndRemoveEntries: UseCases.FileSysObjects.addAndRemoveEntries.html#
.. _normalizeSearchPathLists: UseCases.FileSysObjects.normalizeSearchPathLists.html#


Search for Files, Directories, and Branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  +-----------------------------------------------+-------------------------------------------+
  | UseCase                                       | [doc/source]                              | 
  +===============================================+===========================================+
  | Search bottom up                              | `searchBottomUp`_                         |
  +-----------------------------------------------+-------------------------------------------+
  | Search top down                               | `searchTopDown`_                          |
  +-----------------------------------------------+-------------------------------------------+
  | Search side branch for a hook point           | `searchHookPointForSideBranch`_           |
  +-----------------------------------------------+-------------------------------------------+
  | Search side branch for a hook segment         | `searchHookSliceForSideBranch`_           |
  +-----------------------------------------------+-------------------------------------------+
  | Compare hook for points and slices            | `searchHookDifferencesOfPointsAndSlices`_ |
  +-----------------------------------------------+-------------------------------------------+
  | Iterate a search path list                    | `iterateSearchList`_                      |
  +-----------------------------------------------+-------------------------------------------+
  | Search by literal(L)                          | `search.InUpperTree.by_literal`_          |
  +-----------------------------------------------+-------------------------------------------+
  | Search by glob(G)                             | `search.InUpperTree.by_glob`_             |
  +-----------------------------------------------+-------------------------------------------+
  | Search by regexpr(R)                          | `search.InUpperTree.by_regexpr`_          |
  +-----------------------------------------------+-------------------------------------------+
  | Search by mixed literal+regexpr+glob (LRG)    | `search.InUpperTree.by_LRG`_              |
  +-----------------------------------------------+-------------------------------------------+

.. _searchBottomUp: UseCases.FileSysObjects.branches.searchBottomUp.html#
.. _searchTopDown: UseCases.FileSysObjects.branches.searchTopDown.html#
.. _searchHookPointForSideBranch: UseCases.FileSysObjects.branches.searchHookPointForSideBranch.html#
.. _searchHookSliceForSideBranch: UseCases.FileSysObjects.branches.searchHookSliceForSideBranch.html#
.. _searchHookDifferencesOfPointsAndSlices: UseCases.FileSysObjects.branches.searchHookDifferencesOfPointsAndSlices.html#
.. _iterateSearchList: UseCases.FileSysObjects.branches.iterateSearchList.html#

.. _search.InUpperTree.by_literal: UseCases.FileSysObjects.search.InUpperTree.by_literal.html#
.. _search.InUpperTree.by_glob: UseCases.FileSysObjects.search.InUpperTree.by_glob.html#
.. _search.InUpperTree.by_regexpr: UseCases.FileSysObjects.search.InUpperTree.by_regexpr.html#
.. _search.InUpperTree.by_LRG: UseCases.FileSysObjects.search.InUpperTree.by_LRG.html#

Match on Path Strings
^^^^^^^^^^^^^^^^^^^^^

  +-----------------------------------------------+----------------------------------------------+
  | UseCase                                       | [doc/source]                                 | 
  +===============================================+==============================================+
  | Map side branch for a hook point              | `searchHookPointForSideBranchStr`_           |
  +-----------------------------------------------+----------------------------------------------+
  | Map side branch for a hook segment            | `searchHookSliceForSideBranchStr`_           |
  +-----------------------------------------------+----------------------------------------------+
  | Compare mapping of hook for points and slices | `searchHookDifferencesOfPointsAndSlicesStr`_ |
  +-----------------------------------------------+----------------------------------------------+
  | Iterate the elements of a search path string  | `iteratePathElements`_                       |
  +-----------------------------------------------+----------------------------------------------+

.. _searchHookPointForSideBranchStr: UseCases.FileSysObjects.branches.searchHookPointForSideBranchStr.html#
.. _searchHookSliceForSideBranchStr: UseCases.FileSysObjects.branches.searchHookSliceForSideBranchStr.html#
.. _searchHookDifferencesOfPointsAndSlicesStr: UseCases.FileSysObjects.branches.searchHookDifferencesOfPointsAndSlicesStr.html#
.. _iteratePathElements: UseCases.FileSysObjects.pathstrings.iteratePathElements.html#

Patterns for Library Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  +---------------------------------------------------------------+--------------------------------------+
  | UseCase                                                       | [doc/source]                         | 
  +===============================================================+======================================+
  | Adds an entry to a plist                                      | `addPathToSearchPath`_               |
  +---------------------------------------------------------------+--------------------------------------+
  | Finds a hook for a relative path in plist                     | `findRelPathInSearchPath`_           |
  +---------------------------------------------------------------+--------------------------------------+
  | Iterates over all possible matches                            | `findRelPathInSearchPathIter`_       |
  +---------------------------------------------------------------+--------------------------------------+
  | Finds the topmost hook within a segment of the directory tree | `getTopFromPathString`_              |
  +---------------------------------------------------------------+--------------------------------------+
  | Iterates over all possible matches                            | `getTopFromPathStringIter`_          |
  +---------------------------------------------------------------+--------------------------------------+
  | Create a plist for a segment of the directory tree            | `setUpperTreeSearchPath`_            |
  +---------------------------------------------------------------+--------------------------------------+

.. _addPathToSearchPath: UseCases.FileSysObjects.functions.addPathToSearchPath.html#
.. _findRelPathInSearchPath: UseCases.FileSysObjects.functions.findRelPathInSearchPath.html#
.. _findRelPathInSearchPathIter: UseCases.FileSysObjects.functions.findRelPathInSearchPathIter.html#
.. _getTopFromPathString: UseCases.FileSysObjects.functions.getTopFromPathString.html#
.. _getTopFromPathStringIter: UseCases.FileSysObjects.functions.getTopFromPathStringIter.html#
.. _setUpperTreeSearchPath: UseCases.FileSysObjects.functions.setUpperTreeSearchPath.html#

Project Applications
^^^^^^^^^^^^^^^^^^^^

  +-----------------------------------------------------+------------------------------------------------+
  | UseCase                                             | [doc/source]                                   | 
  +=====================================================+================================================+
  | Unit tests with shared and inherited test dummies   | `<https://pypi.python.org/pypi/epyunit>`_      |
  +-----------------------------------------------------+------------------------------------------------+

  The list is going to be extended when more are published.
