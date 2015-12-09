__author__ = 'dexter'

import ndex.client as nc


def save_cx_to_ndex(cx_stream, ndex_url, username, password):
    ndex = nc.Ndex(ndex_url, username, password)
    ndex.save_new_network_as_cx(cx_stream)



