__author__ = 'dexter'
import cx_helper


class ReachCX:
    def __init__(self, output_stream):
        self.cx = cx_helper.CXHelper(output_stream)
        self.data = None
        self.mode = 'fries'
        self.cx_citation_id = None
        self.citation = None
        self.text_to_support_id_map = {}
        self.reach_sentence_id_to_support_id_map = {}

        # many-to-one map of reach entities to cx nodes
        self.reach_entity_id_to_node_id_map = {}

        # one-to-one map of names (the generated function term name) and node ids
        self.entity_name_to_node_id_map = {}

    def fries_to_cx(self, fries, citation):
        self.citation = citation
        self.cx.start()
        self.data = fries
        self.cx.add_cx_context("bel", "http://belframework.org/schema/1.0/xbel")
        self.cx.emit_cx_context()
        self.handle_citation()
        self.handle_sentences()
        self.handle_entities()
        self.handle_events()
        self.cx.end()

    def handle_citation(self):
        # citation_type, title, contributors, identifier, description
        self.cx_citation_id = self.cx.emit_cx_citation(
            self.citation.get('type'),
            self.citation.get('title'),
            self.citation.get('contributors'),
            self.citation.get('identifier'),
            self.citation.get('description'))

    def handle_sentences(self):
        sentences = self.data.get('sentences')
        for sentence in sentences.get('frames'):
            text = sentence.get('text')
            support_id = self.text_to_support_id_map.get(text)
            if not support_id:
                support_id = self.cx.emit_cx_support(self.cx_citation_id, text)
            frame_id = sentence.get('frame_id')
            self.reach_sentence_id_to_support_id_map[frame_id] = support_id

    def entity_to_function_term(self, entity):
        base_term = entity.get('text')
        ft = None
        name = None
        x_refs = entity.get('xrefs')
        e_type = entity.get('type')
        if x_refs and len(x_refs) > 0:
            x_ref = x_refs[0]
            # base_term = {'name': xref.id, 'prefix': xref.namespace}
            if e_type == 'protein' or e_type == 'gene-or-gene-product':
                ft = {'f': 'bel:proteinAbundance', 'args': [base_term]}
                name = 'p(' + base_term + ')'
            elif e_type == 'simple-chemical':
                ft = {'f': 'bel:abundance', 'args': [base_term]}
                name = 'a(' + base_term + ')'
            else:
                ft = {'f': 'bel:abundance', 'args': [base_term]}
                name = 'a(' + base_term + ')'
        else:
            # no xrefs, just use the name
            # base_term = {'name': entity.text}
            ft = {'f': 'bel:abundance', 'args': [base_term]}
            name = 'a(' + base_term + ')'
        return ft, name

    def handle_entities(self):
        entities = self.data.get('entities')
        for entity in entities.get('frames'):
            function_term, name = self.entity_to_function_term(entity)
            node_id = self.entity_name_to_node_id_map.get(name)
            if not node_id:
                node_id = self.cx.emit_cx_node(name)
                self.entity_name_to_node_id_map[name] = node_id
                function_term['po'] = node_id
                function_term_id = self.cx.emit_cx_function_term(function_term)
            frame_id = entity.get('frame_id')
            self.reach_entity_id_to_node_id_map[frame_id] = node_id

    def handle_events(self):
        events = self.data.get('events')
        for event in events.get('frames'):
            event_type = event.get('type')

            if event_type and event_type == 'activation':
                subtype = event.get('subtype')
                if subtype and subtype == 'negative-activation':
                    interaction = 'bel:decreases'
                else:
                    interaction = 'bel:increases'

                source_id = self.get_argument_id('controller', event)
                target_id = self.get_argument_id('controlled', event)

                if source_id and target_id and interaction:
                    edge_id = self.cx.emit_cx_edge(source_id, target_id, interaction)
                    sentence_id = event.get('sentence')
                    if sentence_id:
                        support_id = self.reach_sentence_id_to_support_id_map.get(sentence_id)
                        if support_id:
                            self.cx.emit_cx_edge_support(edge_id, support_id)

    def get_argument_id(self, argument_label, event):
        for argument in event.get('arguments'):
            label = argument.get('argument_label')
            entity_id = argument.get('arg')
            if label and argument_label == label:
                node_id = self.reach_entity_id_to_node_id_map.get(entity_id)
                return node_id
        return None



