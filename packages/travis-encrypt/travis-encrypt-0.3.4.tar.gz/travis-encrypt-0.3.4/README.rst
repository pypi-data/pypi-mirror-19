.. image:: travis/images/header.png

|travis| |coverage| |dependencies| |codacy| |version| |status| |pyversions| |format| |license|


Travis Encrypt is a Python command line application that provides an easy way to encrypt passwords
and environment variables for use with Travis CI. This application intends to be a replacement for the Travis Ruby client as that client is not maintained and does not provide detail regarding password encryption.

All passwords and environment variables are encrypted with the PKCS1v15 padding scheme until
Travis-CI updates its protocols.

*************
Installation
*************


To install Travis Encrypt simply run the following command in a terminal window::

    $  pip install travis-encrypt

If you would rather install from source, run the following commands in a terminal window::

    $  git clone https://github.com/mandeep/Travis-Encrypt.git
    $  cd Travis-Encrypt
    $  python setup.py install

Travis Encrypt will attempt to install the cryptography package, however the package requires
headers for Python. If installation fails, please see the cryptography installation guide:
https://cryptography.io/en/latest/installation/

******
Usage
******

With Travis Encrypt installed, the command line application can be invoked with the following command and mandatory arguments::

    usage: travis-encrypt [options] github_username repository path

    positional arguments:
        github_username         GitHub username that houses the repository
        repository              Name of the repository whose password requires encryption
        path                    Path to the repository's .travis.yml file

    optional arguments:
        --help                  Show the help message and quit
        --deploy                Encrypt a password for continuous deployment usage
        --env                   Encrypt an environment variable

When the command is entered, the application will issue a prompt where the user can enter
either a password or environment variable. In both cases, the prompt will print 'Password:'.
Once the prompt is answered, Travis Encrypt will write the encrypted password or
environment variable to the given .travis.yml file.

Example of password encryption::

    $  travis-encrypt mandeep Travis-Encrypt /home/user/.travis.yml
    Password:

Example of deployment password encryption::

    $  travis-encrypt --deploy mandeep Travis-Encrypt /home/user/.travis.yml
    Password:

Example of environment variable encryption::

    $  travis-encrypt --env mandeep Travis-Encrypt /home/user/.travis.yml
    Password:

.. |travis| image:: https://travis-ci.org/mandeep/Travis-Encrypt.svg?branch=master
    :target: https://travis-ci.org/mandeep/Travis-Encrypt
.. |coverage| image:: https://img.shields.io/coveralls/mandeep/Travis-Encrypt.svg
    :target: https://coveralls.io/github/mandeep/Travis-Encrypt 
.. |dependencies| image:: https://dependencyci.com/github/mandeep/Travis-Encrypt/badge
    :target: https://dependencyci.com/github/mandeep/Travis-Encrypt
.. |codacy| image:: https://img.shields.io/codacy/grade/16d519300c4d4524a38b385f6a7a2275.svg
    :target: https://www.codacy.com/app/bhutanimandeep/Travis-Encrypt/dashboard
.. |version| image:: https://img.shields.io/pypi/v/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |status| image:: https://img.shields.io/pypi/status/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |format| image:: https://img.shields.io/pypi/format/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |license| image:: https://img.shields.io/pypi/l/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt