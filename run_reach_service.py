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
import ndex.client as nc
import json
import pmc_helper
import reach_helper
import codecs
import reach_cx


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

@route('/test/loadpmcid/<pmc_id>', method='GET')
def load_pmcid(pmc_id):
    # pmc_id = 'PMC3031885'
    current_directory = dirname(abspath(__file__))

    xml_text = pmc_helper.get_pmc_full_text_xml(pmc_id)

    print "got PMC XML"

    fries_json = reach_helper.process_nxml(xml_text, 'fries')

    json_file_path = join(current_directory, "test-files", pmc_id + ".fries.json")

    with codecs.open(json_file_path,'w',encoding='utf8') as f:
        json.dump(fries_json, f)

    output_file_path = join(current_directory, "cx_output", pmc_id + ".bel.cx")

    out = open(output_file_path, "w")

    cx = reach_cx.ReachCX(out)

    cx.fries_to_cx(fries_json,{
        'type' : 'pmid',
        'uri' : None,
        'title' : "fake title",
        'contributors' : [],
        'identifier' : '12729465',
        'description' : ""
    })

    out.close()

    ndex = nc.Ndex(host='http://dev2.ndexbio.org/', username='test', password='test')

    cx_stream = open(output_file_path, 'rb')
    ndex_uuid = ndex.save_cx_stream_as_new_network(cx_stream)

    return ndex_uuid

run(app, host='localhost', port=5603)