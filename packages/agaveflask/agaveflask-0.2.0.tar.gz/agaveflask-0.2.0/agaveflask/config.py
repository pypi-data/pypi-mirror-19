"""Read config files from:
- /service.conf (added by user)
- /etc/service.conf
- CWD/service.conf

"""

from configparser import ConfigParser, NoOptionError, NoSectionError
import os

HERE = os.path.dirname(os.path.abspath(__file__))

class AgaveConfigParser():
    def __init__(self):
        self.parser = ConfigParser()
    def get(self, section, option, default_value=None):
        try:
            return self.parser.get(section, option)
        except (NoOptionError, NoSectionError):
            return default_value


def read_config(conf_file='service.conf'):
    parser = AgaveConfigParser()
    places = ['/{}'.format(conf_file),
              '/etc/{}'.format(conf_file),
              '{}/{}'.format(os.getcwd(), conf_file)]
    place = places[0]
    for p in places:
        if os.path.exists(p):
            place = p
            break
    else:
        raise RuntimeError('No config file found.')
    if not parser.parser.read(place):
        raise RuntimeError("couldn't read config file from {0}"
                           .format(', '.join(place)))
    return parser

Config = read_config()