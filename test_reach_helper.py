__author__ = 'dexter'

import reach_helper
import pmc_helper
import json

xml_text = pmc_helper.get_pmc_full_text_xml('PMC3031885')

print "got PMC XML"

fries_json = reach_helper.process_nxml(xml_text, 'fries')


print json.dumps(fries_json, sort_keys=True, indent=4, separators=(',', ': '))