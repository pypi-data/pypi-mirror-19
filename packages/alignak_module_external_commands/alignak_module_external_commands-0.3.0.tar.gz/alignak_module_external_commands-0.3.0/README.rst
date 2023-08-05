Alignak External commands Module
================================

*Alignak external commands module*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-external-commands.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-external-commands
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-external-commands/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-external-commands/develop
    :alt: Development code static analysis

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-module-external-commands/badge.svg?branch=develop
    :target: https://coveralls.io/r/Alignak-monitoring-contrib/alignak-module-external-commands
    :alt: Development code tests coverage

.. image:: https://badge.fury.io/py/alignak_module_backend.svg
    :target: https://badge.fury.io/py/alignak-module-external-commands
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Short description
-----------------

This module for Alignak opens a commands file as a named pipe and regularly reads the content of this file to interpret as external commands that are forwarded to the Alignak framework.



Installation
------------

The installation of this module will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the modules (eg. *arbiter/modules*).

From PyPI
~~~~~~~~~
To install the module from PyPI:
::

   sudo pip install alignak-module-external-commands


From source files
~~~~~~~~~~~~~~~~~
To install the module from the source files (for developing purpose):
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-module-external-commands
   cd alignak-module-external-commands
   sudo pip install . -e

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*


Configuration
-------------

Once installed, this module has its own configuration file in the */usr/local/etc/alignak/arbiter/modules* directory.
The default configuration file is *mod-external-commands.cfg*. This file is commented to help configure all the parameters.

To configure an Alignak daemon to use this module:

- edit your daemon configuration file
- add your module alias value (`external-commands`) to the `modules` parameter of the daemon




Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-module-external-commands/issues>`_ are the common way to raise an information.
