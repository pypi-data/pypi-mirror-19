README
======

What is this repository for?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command line backup tool which backups local files to Amazon S3.

AES-256 client side encryption support is also available.

Only regular files, symlinks and folders are backed up.

**Requirements**: Linux or a Unix system (or a derivative) having Python
2.7, the Pycrypto and Boto python libraries. If using encryption then at
least 60MB RAM need to be available for the backup tool.

**Tested on**: Mac OS X *El Captian*\ (10.11), Ubuntu 16.04, FreeBSD 9.3
. Most likely will work on a lot more systems.

Installation
~~~~~~~~~~~~

Install From Pip (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install package: ``sudo pip install s3backuptool``

Create a config file based on the `provided
sample <https://bitbucket.org/alexandru_ionica/s3backuptool/raw/master/s3backuptool/config.sample>`__.

Install From Source
^^^^^^^^^^^^^^^^^^^

Fetch
`s3backuptool.py <https://bitbucket.org/alexandru_ionica/s3backuptool/raw/master/s3backuptool/s3backuptool.py>`__
and
`config.sample <https://bitbucket.org/alexandru_ionica/s3backuptool/raw/master/s3backuptool/config.sample>`__
files from source and make the release executable with
``chmod +x s3backuptool.py``

Install dependencies
''''''''''''''''''''

from your distribution's package repositories:


-  for CentOS 6 or RHEL 6 with EPEL repo:
   ``yum install python-crypto2.6 python2-boto``
-  for CentOS 7 or RHEL 7 with EPEL repo:
   ``yum install python2-crypto python2-boto``
-  Ubuntu 12.04 / 14.04 / 16.04:
   ``apt-get install python-boto python-crypto``
-  Debian: ``apt-get install python-boto python-crypto`` ###### using
   pip ``pip install boto pycrypto`` ### Usage: backups ###
-  Edit the config file and adjust as needed.
-  Init the SQLite database(ese) which will store information about
   backed up files. The reason init is manually done is to ensure that
   in the case the database is lost, the user is always notified. Run:
   ``./s3backuptool.py -c config_file initdb``
-  Run the first backup: ``./s3backuptool.py -c config_file backup``

Verbose messages can be enabled with ``--verbose`` or debug can be
enabled with ``--debug``

Usage: restores
^^^^^^^^^^^^^^^

-  If you don't already have a config file then create it and adjust as
   needed so it resembles the config file used to backup files. Pay
   special attention to having the same configuration section(s), S3
   bucket name and path variables or otherwise restores will fail
-  If the system where you are going to restore does not have the
   database which used to store backed up file information then run the
   database init: ``./s3backuptool.py -c config_file initdb`` . This
   will be used to store information about files pending restored and
   also restored files
-  Start restore with: ``./s3backuptool.py -c config_file restore``.
   Once the file selection is complete even if somehow the restore
   fails, you should be able to resume the restore from where it was
   left

Usage: information about backups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  to show all files backed up to AWS S3 run:
   ``./s3backuptool.py -c config_file list_remote``
-  to show statistics about backed up files, run:
   ``./s3backuptool.py -c config_file stats``

Usage: dealing with a corrupted or lost local backed up files database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  if somehow you loose the local database(s) which store information
   about backedup files then you can rebuild the local DB using the
   metadata of the S3 store files, by running:
   ``./s3backuptool.py -c config_file syncdb_remote``

How does it work ?
~~~~~~~~~~~~~~~~~~

The purpose of the local SQLite databse(s)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A SQLite database is used for each "configuration section" (section
defining how to backup files under a certain path). This database stores
metadata about files like last changed time, file size, permissions,
etc. When a backup operation runs file properties will be compared with
the data available in the database and based on this a decision will be
made if a new copy of the file needs to be uploaded to Amazon S3.

Using a local DB provides advantages as the fact that no S3 operations
are need to be performed except for file uploads. Otherwise for each
backed up files, the file properties would have to be fetched from S3
and compared to local files and this operation would be slow (and cost).

Metadata stored in S3
^^^^^^^^^^^^^^^^^^^^^

For each backed up file, properties like last change time, owner, group,
permission modes are saved as S3 metadata attached to the S3 Key.
Otherwise the file content is unchanged and you could directly download
and use the file (except if it's encrypted)

Encryption
^^^^^^^^^^

If desired, files can be encrypted on the client side using
`AES256 <https://en.wikipedia.org/wiki/Advanced_Encryption_Standard>`__
encryption but by default encryption is disabled. If you choose to
enable encryption then each file is encrypted: \* using a different
`salt <https://en.wikipedia.org/wiki/Salt_(cryptography)>`__ and
`initialization
vector(IV) <https://en.wikipedia.org/wiki/Initialization_vector>`__ \*
the original(unencrypted) file size, salt and IV are stored at the
begining of the ecrypted file using the following format: original file
size (8 bytes) + IV (16 bytes) + salt (32 bytes) + encrypted file
content \* only file content is encrypted. File names or metadata like
owner, permissions bits are not encrypted

WARNINGS
~~~~~~~~

Before using this tool please understand that: \* it's a very very new
tool, so there may be lots of bugs lurking \* only regular files,
symlinks and folders are backed up. All other types of files are
ignored. This means the tool is geared at backing up content and less at
doing full system restores (because it ignores things like device files,
sockets, etc)

License
~~~~~~~

GPLv2

Contribution guidelines
~~~~~~~~~~~~~~~~~~~~~~~

Please use 160 character width lines for formatting. Submit pull
requests with patches and adjusted/added unit tests, where needed.

Who do I talk to?
~~~~~~~~~~~~~~~~~

-  Repo owner or admin: Alexandru Ionica alexandru@ionica.eu

Should I use this in production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please understand this is alpha quality software. Use it on your own
risk.


