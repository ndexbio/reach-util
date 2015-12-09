__author__ = 'dexter'

import pmc_helper
import codecs
from os import listdir, makedirs
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext

pmc_id = 'PMC3031885'
current_directory = dirname(abspath(__file__))

pmc_xml = pmc_helper.get_pmc_full_text_xml(pmc_id)

output_file_path = join(current_directory, "test-files", pmc_id + ".pmc.xml")

#out = open(output_file_path, "w")

#out.write(pmc_xml)

with codecs.open(output_file_path,'w',encoding='utf8') as f:
    f.write(pmc_xml)

