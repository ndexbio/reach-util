__author__ = 'dexter'

import reach_helper
import pmc_helper
import reach_cx
from os import listdir, makedirs
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext
import codecs
import json
import ndex.client as nc

pmc_id = 'PMC3031885'
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

print ndex_uuid
print "done"