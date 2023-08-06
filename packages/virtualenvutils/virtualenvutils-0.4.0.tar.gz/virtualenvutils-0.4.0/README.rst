===================
``virtualenvutils``
===================

You can manage virtualenv based **utilities** with this utility.  Its
primary use in addition to installing and updating is creating links
(in ``/usr/local/bin``) for utilities that are installed in separate
virtualenvs.

Originally it only created alias definitions that could be 'sourced' into bash.
But those aliases were difficult to use from non-login shells (and crontab etc).
It still can generate those aliases, but only does so for those commands for which it cannot find a link in ``/usr/local/bin/``

In such a setup, where you have a separate virtualenv for each
utility, you don't want to extend your path with the ``bin`` directory
of each of the virtualenvs, as that gives you:

- a long PATH
- multiple python executables in your PATH
- all utilties that are a result of installing some Python package dependency
  and for which you might want to use a different version (or not all).

If during install / update ``/usr/local/bin`` cannot be written to,
the program will call ``sudo ln -s /usr/local/bin/yourutil
/opt/util/yourutil/bin/yourutil`` (or similar) that will prompt you
for the root privilages password.

Of course directly specifying the full path to your virtualenv based
utility works as well.



Aliases
=======

**This is no longer needed.**

``virtualenvutils alias dir1 dir2`` scans directories, non-recursive, under ``dir1`,
``dir2`` for virtualenvs. Any directory containing ``bin``, ``lib``, ``include`` subdirectories as well as a file ``bin/activate`` is considered a virtualenv.

For any of those virtualenvs it does one of following (checked in this order):

- if there is a virtualenvutils.conf file it is loaded to determine
  the utilties and possibly their mapping.
- if the name of the directory under ``dir1``, etc., is e.g. ``do_xyx``,
  and ``dir1/do_xyz/bin/do_xyz`` exists and is executable then this is
  the utility
- if there is no matching name, then all of the executable files under
  ``bin`` except those matching ``activate*``, ``easy_install*``,
  ``pip*``, ``python*``, ``wheel*`` are considered utilities, unless
  they have extensions matching ".so", ".py", or ".pyc".

the utility then generates aliases for all utilities found this way,
making sure they are unique if added by the last method, and writes
those alias definitions to stdout. Any error go to stderr.

Other functionalities include:

- updating all packages for all virtualenvs

see ``virtualenvutils --help`` for the full list of subcommands

``virtualenvutils.conf``
------------------------

The ``virtualenvutils.conf`` file, if provided, has to be in
the toplevel directory of the virtualenv (i.e. next to ``bin``,
``include`` and ``lib`` and consist of single line with or without a
colon (:).

If there is no colon, then the line is considered to be the
name of an executable file under that virtualenvs ``bin``.

If there is a colon, the part before the colon is considered the
name for executable under ``bin``, for which the executable name is
the part behind the colon.


Example
=======

You want to install docker-compose in a virtualenv. If you do::

   mkvirtualenv -p /opt/python3/bin/python /opt/util/docker-compose
   source !$/bin/activate
   pip install docker-compose
   deactivate

you will need to call it with::

   /opt/util/docker-compose/bin/docker-compose

If you would have specified a different final  directory::

   mkvirtualenv -p /opt/python3/bin/python /opt/util/compose
   source !$/bin/activate
   pip install docker-compose
   deactivate

you will need to use::

   /opt/util/compose/bin/docker-compose


The above can resp. be done using ``virtualenvutils`` by using::

   virtualenvutils install /opt/util/docker-compose

and::

   virtualenvutils install /opt/util/compose --pkg docker-compose

respectively. In both instances a link `/usr/local/bin/docker-compose`
will be created that will be able to start your utility.

Installing virtualenvutils
==========================

To bootstrap ``virtualenvutils``::

   mkvirtualenv -p /opt/python3/bin/python /opt/util/virtualenvutils
   source !$/bin/activate
   pip install virtualenvutils
   virtualenvutils update virtualenvutils  # this will create the link
   deactivate

after which you can use plain ``virtualenvutils`` as long as
``/usr/local/bin`` is in your PATH.

Updating existing virtualenvs
=============================

You can update all packages for all virtualenv utilities (under `/opt/util`) by using:

   virtualenvutils update /opt/util

The arguments to `update` are checked to see if they are virtualenvs. If they
are they get update on an individual basis. If they are not (as in the above
example) each of their subdirs are checked to be virtualenvs (non-recursive).

Installing a new util
=====================

You can install one or more new virtualenv based utilities using
something like:

  virtualenvutils install /opt/util/{docker-compose,ruamel.yaml.cmd}

You can use ``--pkg``
to give a package name that differs from the final part of the path
(in which case you can of course only specify one path), and with
``--python /opt/python/3/bin/python`` you can explicitly
specify the python version to use.

Don't forget that you probably have to logout and login for if you set
your aliases through as scan initiated in ``.bashrc``, before you
can use the commands.
