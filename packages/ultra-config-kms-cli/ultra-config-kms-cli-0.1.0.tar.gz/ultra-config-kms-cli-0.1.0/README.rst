===============================
ultra-config-kms-cli
===============================


.. image:: https://img.shields.io/pypi/v/ultra_config_kms_cli.svg
        :target: https://pypi.python.org/pypi/ultra_config_kms_cli

.. image:: https://img.shields.io/travis/Apptimize-OSS/ultra_config_kms_cli.svg
        :target: https://travis-ci.org/Apptimize-OSS/ultra_config_kms_cli

.. image:: https://readthedocs.org/projects/ultra-config-kms-cli/badge/?version=latest
        :target: https://ultra-config-kms-cli.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Apptimize-OSS/ultra_config_kms_cli/shield.svg
     :target: https://pyup.io/repos/github/Apptimize-OSS/ultra_config_kms_cli/
     :alt: Updates


A simple cli package for easily updating ECS task definition files with secrets


* Free software: MIT license
* Documentation: https://ultra-config-kms-cli.readthedocs.io.


Documentation
-------------

You will need to install the package dependencies first,
see the Installation section for details.

To build and open the documentation simply run:

.. code-block:: bash

    bin/build-docs

Installation
------------

If you need to install pyenv/virtualenvwrapper you can run the `bin/setup-osx` command
Please note that this will modify your bash profile

Assuming you have virtualenv wrapper installed

.. code-block:: bash

    mkvirtualenv ultra-config-kms-cli
    workon ultra-config-kms-cli
    pip install -r requirements_dev.txt
    pip install -e .

Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

