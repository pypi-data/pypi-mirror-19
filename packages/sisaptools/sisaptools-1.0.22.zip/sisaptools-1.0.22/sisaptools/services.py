# -*- coding: utf8 -*-

"""
Importació de services des de json.
"""

import json


pth = os.path.dirname(os.path.abspath(__file__))
json_file = '{}/services.json'.format(pth)

all_json = json.load(open(json_file))
DB_INSTANCES = all_json['db_instances']
DB_CREDENTIALS = all_json['db_credentials']
REDIS_INSTANCES = all_json['redis_instances']
MAIL_SERVERS = all_json['mail_servers']
