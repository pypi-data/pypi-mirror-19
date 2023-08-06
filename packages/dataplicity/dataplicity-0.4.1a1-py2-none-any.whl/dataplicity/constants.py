from __future__ import print_function
from __future__ import unicode_literals

from os import environ

CONF_PATH = "/etc/dataplicity/dataplicity.conf"
SERVER_URL = environ.get('DATAPLICITY_API_URL', "https://api.dataplicity.com")
M2M_URL = environ.get('DATAPLICITY_M2M_URL', "wss://m2m.dataplicity.com/m2m/")
SERIAL_LOCATION = '/opt/dataplicity/tuxtunnel/serial'
AUTH_LOCATION = '/opt/dataplicity/tuxtunnel/auth'
