__author__ = 'dexter'

from os import listdir, makedirs
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext
#import ndex.client as nc
import json
import reach_cx


current_directory = dirname(abspath(__file__))
test_file_path = join(current_directory, "test-files", "PMC3031885.fries.json")
file = open(test_file_path, "r")
data = json.load(file)
file.close()

output_file_path = join(current_directory, "cx_output", "test.PMC3031885.fries.bel.cx")

out = open(output_file_path, "w")

cx = reach_cx.ReachCX(out)

cx.fries_to_cx(data,{
    'type' : 'pmid',
    'uri' : None,
    'title' : "fake title",
    'contributors' : [],
    'identifier' : '12729465',
    'description' : ""
})