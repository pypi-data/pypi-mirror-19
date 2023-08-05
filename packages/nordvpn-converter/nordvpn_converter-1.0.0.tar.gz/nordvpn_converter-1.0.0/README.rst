===============================
NordVPN Configuration Converter
===============================



.. image:: https://drone.io/bitbucket.org/cnavalici/nordvpn-converter/status.png
        :target: https://drone.io/bitbucket.org/cnavalici/nordvpn-converter

.. image:: https://img.shields.io/pypi/v/nordvpn_converter.svg
        :target: https://pypi.python.org/pypi/nordvpn_converter

.. image:: https://img.shields.io/travis/cnavalici/nordvpn_converter.svg
        :target: https://travis-ci.org/cnavalici/nordvpn_converter

.. image:: https://readthedocs.org/projects/nordvpn-converter/badge/?version=latest
        :target: https://nordvpn-converter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/cnavalici/nordvpn_converter/shield.svg
     :target: https://pyup.io/repos/github/cnavalici/nordvpn_converter/
     :alt: Updates


Purpose
-------

The main goal of this small script is to convert the OpenVPN configuration files (provided by the NordVPN_ service) into
NetworkManager compatible files.

.. _NordVPN: https://nordvpn.com/


* Free software: GNU General Public License v3
* Documentation: https://nordvpn-converter.readthedocs.io.


Features
--------

* Bulk conversion done in a matter of seconds

How to install
--------------

System-wide
===========

.. code-block:: bash

   pip3 install nordvpn_converter

Virtual environment
===================

.. code-block:: bash

   virtualenv --python=python3 nordvpn_converter
   cd nordvpn_converter
   pip install nordvpn_converter



How to use
--------------------------------------------

Grab the required files
=======================

In order to generate the compatible NetworkManager files, you have to login to your NordVPN account, go for **My Account** section, **Download Area**, **Linux** and download *.OVPN configuration files* and *CA & TLS certificates*.

After this, you're gonna end up with 2 archives, **config.zip** and **ca_and_tls_auth_certificates.zip**.


Create a new folder and unpack them there:

.. code-block:: bash

   mkdir ~/NordVPN_Data
   unzip -d ~/NordVPN_Data ~/Downloads/config.zip
   unzip -d ~/NordVPN_Data ~/Downloads/ca_and_tls_auth_certificates.zip

Let's assume that you have now the following structure:

.. code-block:: bash

    ~/NordVPN_Data/CA\ and\ TLS\ auth\ certificates/*key
    ~/NordVPN_Data/CA\ and\ TLS\ auth\ certificates/*crt
    ~/NordVPN_Data/*.ovpn


Run the conversion
==================

The regular help information is available:

.. code-block:: bash

    usage: nordvpn_converter [-h] [--source SOURCE] [--destination DESTINATION]
                         [--certs CERTS] [--user USER] [-v] [--version]

    This is a simple conversion tool.

    optional arguments:
      -h, --help            show this help message and exit
      --source SOURCE       Source folder for ovpn config files
      --destination DESTINATION
                        Destination folder for output files
      --certs CERTS         Source folder for certificates
      --user USER           Username used for the NordVPN connection
      -v, --verbose         Verbose mode
      --version             show program's version number and exit

And based on our example:

.. code-block:: bash

    nordvpn_converter --source ~/NordVPN_Data --certs ~/NordVPN_Data/CA\ and\ TLS\ auth\ certificates --destination /tmp/output --user jbravo

Just note that the *user* is not the local one, but the NordVPN one. The files will be automatically generated with the current local username.

The *ouput* folder will contain now a lot of NetworkManager compatible files.

Install the NetworkManager files
--------------------------------

Move the output files into NetworkManager connections folder and then process them.

.. code-block:: bash

   cp /tmp/output/* /etc/NetworkManager/system-connections
   chmod 600 *
   nmcli conn reload

Now you should be able to see those connections also in the NetworkManager applet from your graphical environment.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

