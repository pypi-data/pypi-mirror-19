Extended Filesystems - Network Features
=======================================

**ATTENTION**: This module is currently experimental, not yet active used in production releases, just included, and may change.

The main intention is to find a common and canonical form of filepathnames, which cover more
than the literally 'local-only' addressing, but still does not burden the full scale of 
possible cases of application specific syntaxes and URI schemes.
Thus the defined function 'normpathX' extends the standard function 'os.path.normpath' with awareness
of an optional network prefix of the pathname.

The current supported types of applications are network specific addressing of remote filesystems
with location information only.
This comprises common information provided for the most filesystems as well as for the 
most common URIs.
The current scope comprises:

* Filesystems based on naming conventions from IEEE-1003.1

* Filesystems based on SMB/CIFS naming conventions

* Native filesystems for Linux, Unix, BSD

* Native filesystems for Apple MacOS

* Native filesystems for Microsoft Windows

* URIs for the schemes http, https, ftp, file, smb, cifs,
  where the subset for the location attributes is supported

The created result comprises the generic location information, 
but avoids specific attributes like access credentials.

* scheme - an access protocol onto the resource

* host[:port] - the port for the access onto the resource
  which may include the access-port of a specific 
  storage/filesystem gateway

* pathname - the local resource locator on the access location



The function splits the provided URIs and known application specific definitions into a tuple 
consisting of it's parts. 

The standard path address is kept and passed through to 'os.path.normpath' - for now on the local system
later versions will include appropriate parameters for the target filesystem including the path-prefix
of the remote working directory.

* Linux and UNIX:

  * IEEE Std 1003.1(TM), 2013 Edition; Chapter 4.12::

     _            //host/path/name
                    \__/\________/
                     |          |
                 authority    path
                 ____|____    __|__
                /         \  /     \
     ( 'share', host[:port], pathname, )


     //hostname/local/filesystem/path => ( 'share', 'hostname', '/local/filesystem/path', ) 

    Valid applications are here SMBFS/CIFS, and RFS.

  * SMB/CIFS the same as for previous IEEE Std 1003.1, with additional support for
    backslashes '\\'

  * Standard local filesystem::

     _            /path/name
                  \________/
                      |
                     path
                    __|__
                   /     \
     ( 'local', None, pathname, )


     /local/filesystem/path => ( 'local', None, '/local/filesystem/path', ) 

* Microsoft(TM) Windows:

  * SMB/CIFS shares, with additional support for slashes '/'::

     _            \\host\path\name
                    \__/\________/
                     |          |
                 authority    path
                 ____|____    __|__
                /         \  /     \
     ( 'share', host[:port], pathname, )

     \\hostname\local\filesystem\path => ( 'share', 'hostname', '\local\filesystem\path', )

  * Standard local filesystem, with additional support for slashes '/'::

     _           [<drive>:]\path\name
                 \__________________/
                          |
                        path
                        __|__
                       /     \
     ( 'local', None, pathname, )


     [<drive>:]\local\filesystem\path => ( 'local', None, '[<drive>:]/local/filesystem/path', ) 

* Mac-OS:

  * Current same as for Linux/Unix.

* Cygwin:

  * Set of Linux/Unix

  * Set of Microsoft Windows

  * Cygwin specifci extensions - ffs.

* The special case of a URI for local files is resolved to::

     _ file:///path/name
       \__/   \________/
         |       |
       scheme    path
         |        \___
         |            \
         |          __|__
        / \        /     \
     ( 'file', None, pathname, )

     file:///local/filesystem/path => ( 'file', None, '/local/filesystem/path', )  

* The URI definition as defined in the RFC3986 is used as base::

    The following are two example URIs and their component parts:

       foo://example.com:8042/over/there?name=ferret#nose
       \_/  \______________/\_________/ \_________/ \__/
        |           |            |            |       |
     scheme     authority       path        query  fragment
        |   _____________________|__
       / \ /                        \
       urn:example:animal:ferret:nose

  The URIs based on RFC3986 are supported by the following subset. Additional attributes
  are ignored and stripped off within the result.
  This design decision is focused on the position information of resources stored on 
  filesystems only.
  ::

     scheme://host[:port]/path/name
     \____/   \_________/\________/
        |          |          |
     scheme    authority    path
        |      ____|____    __|__
       / \    /         \  /     \
     ( urn,   host[:port], pathname, )

  Examples are::

     http://hostname/path/name => ( 'http', 'hostname', '/path/name', )
     https://hostname/path/name => ( 'https', 'hostname', '/path/name', )
     ftp://hostname/path/name => ( 'ftp', 'hostname', '/path/name', )
     smb://hostname/path/name => ( 'smb', 'hostname', '/path/name', )
     cifs://hostname/path/name => ( 'cifs', 'hostname', '/path/name', )

  Specific attributes like credentials are subject to coming releases.


**See Also**:

* IEEE Std 1003.1(TM), 2013 Edition; Chapter 4.12 @ `<http://www.opengroup.org>`_:
    `<http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html>`_

* Microsoft SMB Protocol and CIFS Protocol Overview  @ `<https://technet.microsoft.com>`_:
    `<https://msdn.microsoft.com/en-us/library/windows/desktop/aa365233%28v=vs.85%29.aspx>`_

* Common Internet File System @ `<https://technet.microsoft.com>`_:
    `<https://technet.microsoft.com/en-us/library/cc939973.aspx>`_

* IETF - RFCs @ `<http://tools.ietf.org/html>`_:
    `RFC1808 <http://tools.ietf.org/html/rfc1808>`_, 
    `RFC1738 <http://tools.ietf.org/html/rfc1738>`_,
    `RFC2396 <http://tools.ietf.org/html/rfc2396>`_,
    `RFC2648 <http://tools.ietf.org/html/rfc2648>`_,
    `RFC3986 <http://tools.ietf.org/html/rfc3986>`_,
    `RFC4122 <http://tools.ietf.org/html/rfc4122>`_,
    `RFC6570 <http://tools.ietf.org/html/rfc6520>`_,
    `RFC7320 <http://tools.ietf.org/html/rfc7320>`_

* From Wikipedia, the free encyclopedia - Path (computing): 
    `<https://en.wikipedia.org/wiki/Path_%28computing%29>`_
