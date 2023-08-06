s2k
===============================

version number: 1.0
author: Haden Pike

Overview
--------

Send files to your Kindle email.

Installation
------------

To install use pip:

    $ pip install s2k


Or clone the repo:

    $ git clone https://github.com/hadenpike/s2k.git
    $ python setup.py install

Usage
-----

$ s2k -h
usage: s2k [-h] [-cf CONFIGFILE] [-c] f [f ...]

Send files to your Kindle email

positional arguments:
  f                     Files to send to Kindle.

optional arguments:
  -h, --help            show this help message and exit
  -cf CONFIGFILE, --configfile CONFIGFILE
                        Location of configuration file.
  -c, --convert         Request the Kindle service to convert files to
                        internal format.

Configuration
-------------

First, follow the instructions [here](https://www.amazon.com/gp/help/customer/display.html?nodeId=201974220) to view your Send to Kindle email address. The default location of the configuration file is ~/.s2krc. Create it if it does not exist. The configuration file is written in the standard INI format, and supports the following values. Any key without a default value is required.

| Option | Type | Description | Default |
| ----- | ---- | ----------- | ------- |
| from | string | The email address to send from | The $EMAIL environment variable |
| to | string | Your Kindle Email address | |
| server | string | The address of the SMTP server | |
| port | integer | The port the SMTP server is listening on | 587 |
| username | string | The username to log into the SMTP server | |
| password | string | The password to log into the SMTP server | |

