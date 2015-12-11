__author__ = 'david'

from os.path import dirname, abspath, join
import ndex.client as nc

pmc_id = 'PMC3031885'
current_directory = dirname(abspath(__file__))

cx_filename = join(current_directory, 'cx_output', 'test.'+pmc_id+'.fries.bel.cx')

ndex = nc.Ndex(host='http://dev2.ndexbio.org', username='test', password='test')

cx_stream = open(cx_filename, 'rb')

ndex_uuid = ndex.save_cx_stream_as_new_network(cx_stream)

cx_stream.close()

print ndex_uuid
print 'done'

