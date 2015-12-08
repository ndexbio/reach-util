__author__ = 'dexter'

__author__ = 'dexter'

# This script is called from the command line to run the enrichment server with the persisted e_sets
#
# The script reads all of the e_sets and then starts the bottle server
#
# The optional argument 'verbose' specifies verbose logging for testing
#

#
# python run_e_service.py
#
# python run_e_service.py --verbose
#

# body

import argparse
from bottle import route, run, hook, response, template, default_app, request, post, abort
from os import listdir, makedirs
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext
#import ndex.client as nc
import json


parser = argparse.ArgumentParser(description='run the indra service')

parser.add_argument('--verbose', dest='verbose', action='store_const',
                    const=True, default=False,
                    help='verbose mode')

arg = parser.parse_args()

if arg.verbose:
    print "Starting reach service in verbose mode"
else:
    print "Starting reach service"

app = default_app()
app.config['verbose'] = arg.verbose

#app.config['ndex'] = nc.Ndex()

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/test/fries', method='GET')
def reach_fries_test_query():
    current_directory = dirname(abspath(__file__))
    test_file_path = join(current_directory, "test-files", "fries_example.json")
    file = open(test_file_path, "r")
    data = json.load(file)
    file.close()
    return data

run(app, host='localhost', port=5603)