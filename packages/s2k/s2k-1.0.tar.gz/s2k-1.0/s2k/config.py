from cStringIO import StringIO
from os import environ

from configobj import ConfigObj
from validate import Validator

spec = StringIO(
"""from=string(default="{0}")
to=string
username=string
password=string
server=string
port=integer(default=587)
""".format(environ['EMAIL']))

def initialize(configfile):
    """Initializes and validates the configuration file.

    @returns (valid, config): The validation status and the parsed config object.
    @rtype: tuple
    """

    v = Validator()
    config = ConfigObj(configfile, configspec=spec)
    res = config.validate(v)
    return (res, config)

