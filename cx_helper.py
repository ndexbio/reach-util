__author__ = 'dexter'

import json
import time


class CXHelper:
    def __init__(self, output_stream):
        self.out = output_stream
        self.contexts = {}
        self.citation_id_counter = 0
        self.support_id_counter = 0
        self.edge_id_counter = 0
        self.node_id_counter = 0
        self.update_time = -1
        self.aspect_names = ["@context","citations","edgeAttributes",
                             "edgeCitations","edgeSupports","edges",
                             "networkAttributes","nodeAttributes","nodeCitations",
                             "nodeSupports","nodes","provenanceHistory","supports"]


    def emit(self, cx_object, separate=True):
        if separate:
            self.out.write(', ')
            self.out.write('\n')
        json.dump(cx_object, self.out)

    def start(self):
        self.update_time = int(round(time.time() * 1000))
        self.out.write('[')
        self.out.write('\n')
        self.emit_number_verification()
        self.emit_pre_metadata()

    def end(self):
        self.emit_post_metadata()
        self.out.write('\n')
        self.out.write(']')

    def add_cx_context(self, prefix, uri):
        self.contexts[prefix] = uri

    def emit_number_verification(self):
        self.emit({'numberVerification': [{'longNumber': 281474976710655}]}, False)

    def emit_pre_metadata(self):
        aspect_meta_data = []
        for aspect_name in self.aspect_names:
            aspect_meta_data.append({"name" : aspect_name,
                                     "consistencyGroup" : 1,
                                     "version" : "1.0",
                                     "lastUpdate" : self.update_time})
        self.emit({'metaData' : aspect_meta_data})

    def emit_post_metadata(self):
        aspect_meta_data = [
            {"name" : "nodes",
             "idCounter": self.node_id_counter},
            {"name" : "edges",
             "idCounter": self.edge_id_counter},
            {"name" : "supports",
             "idCounter": self.support_id_counter},
            {"name" : "citations",
             "idCounter": self.citation_id_counter},
        ]
        self.emit({'metaData' : aspect_meta_data})

    def emit_cx_fragment(self, aspect_name, body):
        self.emit({aspect_name: [body]})

    def emit_cx_context(self):
        self.emit_cx_fragment('@context', self.contexts)

    def emit_cx_citation(self, citation_type, title, contributors, identifier, description):
        self.citation_id_counter += 1
        self.emit_cx_fragment(
            'citations', {
                '@id': self.citation_id_counter,
                'dc:title': title,
                'dc:contributor': contributors,
                'dc:identifier': identifier,
                'dc:type': citation_type,
                'dc:description': description,
                'attributes': []
            })
        return self.citation_id_counter

    def emit_cx_support(self, cx_citation_id, text):
        self.support_id_counter += 1
        self.emit_cx_fragment(
            'supports', {
                '@id': self.support_id_counter,
                'citation': cx_citation_id,
                'text': text,
                'attributes': []
            })
        return self.support_id_counter

    def emit_cx_edge_w_id(self, id, source_id, target_id, interaction ):
        body = {
            '@id': id,
            's': source_id,
            't': target_id,
            'i': interaction
        }
        self.emit_cx_fragment('edges', body)
        return id

    def emit_cx_edge(self, source_id, target_id, interaction):
        self.edge_id_counter += 1
        self.emit_cx_fragment(
            'edges', {
                '@id': self.edge_id_counter,
                's': source_id,
                't': target_id,
                'i': interaction
            })
        return self.edge_id_counter

    def emit_cx_network_attribute(self, name, value, att_type=None):
        body = {
            'n': name,
            'v': value
        }
        if type:
            body['t'] = att_type
        self.emit_cx_fragment('networkAttributes', body)


    def emit_cx_edge_attribute(self, edge_id, name, value, att_type=None):
        body = {
            'po': edge_id,
            'n': name,
            'v': value
        }
        if type:
            body['t'] = att_type
        self.emit_cx_fragment('edgeAttributes', body)

    def emit_cx_node_w_id(self, id, name, represents ):
        body = {
            '@id': id,
            'n': name,
        }
        if represents:
            body['r'] = represents
        self.emit_cx_fragment('nodes', body)
        return id

    def emit_cx_node(self, node_name):
        self.node_id_counter += 1
        self.emit_cx_fragment(
            'nodes', {
                '@id': self.node_id_counter,
                'n': node_name
            })
        return self.node_id_counter

    def emit_cx_node_attribute(self, node_id, name, value, att_type=None):
        body = {
            'po': node_id,
            'n': name,
            'v': value
        }
        if type:
            body['t'] = att_type

        self.emit_cx_fragment('nodeAttributes', body)

    def emit_cx_function_term(self, function_term):
        self.emit_cx_fragment('functionTerms', function_term)

    def emit_cx_node_citation(self, node_id, citation_id):
        self.emit_cx_fragment(
            'nodeCitations',
                {
                    "citations": [citation_id],
                    "po" : [node_id]
                }
            )

    def emit_cx_edge_citation(self, edge_id, citation_id):
        self.emit_cx_fragment(
            'edgeCitations',{
                    "citations": [citation_id],
                    "po" : [edge_id]
                }
            )

    def emit_cx_node_support(self, node_id, support_id):
        self.emit_cx_fragment(
            'nodeSupports',
                {
                    "supports": [support_id],
                    "po" : [node_id]
                }
            )

    def emit_cx_edge_support(self, edge_id, support_id):
        self.emit_cx_fragment(
            'edgeSupports',
                {
                    "supports": [support_id],
                    "po" : [edge_id]
                }
            )