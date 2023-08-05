#!/usr/bin/env python
'''Common tests across-software for NI-DM export.
The software-specific test classes must inherit from this class.

@author: Camille Maumet <c.m.j.maumet@warwick.ac.uk>, Satrajit Ghosh
@copyright: University of Warwick 2014
'''

import os
import rdflib
import re
import numpy as np
import json
import glob

import logging

# Append parent script directory to path
RELPATH = os.path.dirname(os.path.abspath(__file__))

from nidmresults.objects.constants_rdflib import *
from nidmresults.owl.owl_reader import OwlReader
from rdflib.namespace import RDF
from rdflib.graph import Graph

logger = logging.getLogger(__name__)


class TestResultDataModel(object):

    def get_readable_name(self, owl, graph, item):
        if isinstance(item, rdflib.term.Literal):
            if item.datatype:
                typeStr = graph.qname(item.datatype)
            else:
                typeStr = ''
            if typeStr:
                typeStr = "(" + typeStr + ")"
            name = "'" + item + "'" + typeStr
        elif isinstance(item, rdflib.term.URIRef):
            # Look for label
            # name = graph.label(item)
            name = owl.graph.qname(item)

            if name.startswith("ns"):
                # Namespace is not declared in the owl file, try with example
                # graph (e.g. for niiri)
                name = graph.qname(item)

            if not name.startswith("niiri"):
                m = re.search(r'\d\d\d\d$', name)
                # alphanumeric identifier
                if m is not None:
                    name += " (i.e. " + \
                        owl.get_label(item).split(":")[1] + ")"
        else:
            name = "unsupported type: " + item
        return name

    def get_alternatives(self, owl, graph, s=None, p=None, o=None):
        found = ""

        for (s_in,  p_in, o_in) in graph.triples((s,  p, o)):
            if not o:
                if not o_in.startswith(str(PROV)):
                    found += "; " + self.get_readable_name(owl, graph, o_in,)
            if not p:
                if not p_in.startswith(str(PROV)):
                    found += "; " + self.get_readable_name(owl, graph, p_in)
            if not s:
                if not s_in.startswith(str(PROV)):
                    found += "; " + self.get_readable_name(owl, graph, s_in)
        if len(found) > 200:
            found = '<many alternatives>'
        else:
            found = found[2:]
        return found

    # FIXME: Extend tests to more than one dataset (group analysis, ...)

    '''Tests based on the analysis of single-subject auditory data based on
    test01_spm_batch.m using SPM12b r5918.

    @author: Camille Maumet <c.m.j.maumet@warwick.ac.uk>, Satrajit Ghosh
    @copyright: University of Warwick 2014
    '''

    def setUp(self, parent_gt_dir=None):
        self.my_execption = ""
        self.gt_dir = parent_gt_dir
        self.ex_graphs = dict()

    def load_graph(self, ttl_name):
        if ttl_name not in self.ex_graphs:
            ttl = ttl_name
            test_dir = os.path.dirname(ttl)

            configfile = os.path.join(test_dir, 'config.json')
            if not os.path.isfile(configfile):
                configfile = os.path.join(
                    os.path.abspath(
                        os.path.join(test_dir, os.pardir)), 'config.json')

            with open(configfile) as data_file:
                metadata = json.load(data_file)
            try:
                gt_file = [os.path.join(self.gt_dir, metadata["version"], x)
                           for x in metadata["ground_truth"]]
            except:
                # This part should be removed once SPM can modify json files
                gt_file = [os.path.join(self.gt_dir, metadata["versions"][0],
                           x)
                           for x in metadata["ground_truth"]]
            inclusive = metadata["inclusive"]
            if "version" in metadata:
                version = metadata["version"]
            else:
                # FIXME: this will be removed once spm json reader is fixed
                version = metadata["versions"][0]
            name = ttl.replace(test_dir, "")

            self.ex_graphs[ttl_name] = ExampleGraph(
                name, ttl, gt_file, inclusive, version)

        return self.ex_graphs[ttl_name]

        # Current script directory is test directory (containing test data)
        # self.test_dir = os.path.dirname(os.path.abspath(
        # inspect.getfile(inspect.currentframe())))

    def print_results(self, res):
        '''Print the results query 'res' to the console'''
        for idx, row in enumerate(res.bindings):
            rowfmt = []
            print("Item %d" % idx)
            for key, val in sorted(row.items()):
                rowfmt.append('%s-->%s' % (key, val.decode()))
            print('\n'.join(rowfmt))

    def successful_retreive(self, res, info_str=""):
        '''Check if the results query 'res' contains a value for each field'''
        if not res.bindings:
            self.my_execption = info_str + """: Empty query results"""
            return False
        for idx, row in enumerate(res.bindings):
            for key, val in sorted(row.items()):
                logging.debug('%s-->%s' % (key, val.decode()))
                if not val.decode():
                    self.my_execption += "\nMissing: \t %s" % (key)
                    return False
        return True

        # if not self.successful_retreive(self.spmexport.query(query),
        #'ContrastMap and ContrastStandardErrorMap'):
        #     raise Exception(self.my_execption)

    def _replace_match(self, graph1, graph2, rdf_type):
        """
        Match classes of type 'rdf_type' across documents based on attributes.
        """

        # Retreive objects of type 'rdf_type' (e.g. prov:Entities)
        g1_terms = set(graph1.subjects(RDF.type, rdf_type))
        g2_terms = set(graph2.subjects(RDF.type, rdf_type))

        activity = False
        agent = False
        MIN_MATCHING = 2
        # For maps at least 4 attributes in common are needed for
        # matching (to deal with nifti files where format and
        # inCoordinateSpace might be the same for all)
        MIN_MAP_MATCHING = 4

        if rdf_type == PROV['Activity']:
            activity = True
        elif rdf_type == PROV['Entity']:
            # FIXME: This would be more efficiently done using the prov owl
            # file
            g1_terms = g1_terms.union(set(
                graph1.subjects(RDF.type, PROV['Bundles'])))
            g1_terms = g1_terms.union(set(
                graph1.subjects(RDF.type, PROV['Coordinate'])))
            g1_terms = g1_terms.union(set(
                graph1.subjects(RDF.type, PROV['Person'])))
            g2_terms = g2_terms.union(set(
                graph2.subjects(RDF.type, PROV['Bundles'])))
            g2_terms = g2_terms.union(
                set(graph2.subjects(RDF.type, PROV['Coordinate'])))
            g2_terms = g2_terms.union(
                set(graph2.subjects(RDF.type, PROV['Person'])))
        elif rdf_type == PROV['Agent']:
            agent = True

        for g1_term in g1_terms:
            min_matching = MIN_MATCHING

            # Look for a match in g2 corresponding to g1_term from g1
            g2_match = dict.fromkeys(g2_terms, 0)
            coord_space_found = False
            format_found = False

            for p, o in graph1.predicate_objects(g1_term):
                logging.debug("Trying to find a match for " +
                              str(graph1.qname(g1_term)) + " " +
                              str(graph1.qname(p)) + " " +
                              str(o))

                if p == NIDM_IN_COORDINATE_SPACE:
                    coord_space_found = True
                if p == DCT['format']:
                    format_found = True
                if coord_space_found and format_found:
                    min_matching = MIN_MAP_MATCHING

                # FIXME: changed "not activity" to "activity" but maybe this
                # could cause issues later on? and condition removed altogether
                # if activity or \
                #        (isinstance(o, rdflib.term.Literal) or p == RDF.type):
                # if graph2.subjects(p, o):
                for g2_term in \
                        (x for x in graph2.subjects(p, o) if x in g2_match):
                    g2_match[g2_term] += 1
                    logging.debug(
                        "Match found with " + str(graph1.qname(g2_term)))
                # else:
                # print(sum(g2_match.values()))
                    # logging.debug("NO --- Match found")

                # If o is a string that is likely to be json check if we have
                # an equivalent json string
                same_json_array = False
                close_float = False
                if hasattr(o, 'datatype') and o.datatype == XSD['string']:
                    for g2_term, g2_o in graph2.subject_objects(p):
                        same_json_array, close_float, same_str = \
                            self._same_json_or_float(o, g2_o)
                        if same_json_array or close_float or same_str:
                            g2_match[g2_term] += 1
                            logging.debug("Match found with " +
                                          str(graph1.qname(g2_term)))

            if activity or agent:
                for s, p in graph1.subject_predicates(g1_term):
                    for g2_term in graph2.objects(s, p):
                        # We don't want to match agents to activities
                        if g2_term in g2_match:
                            g2_match[g2_term] += 1

            match_found = False
            g2_matched = set()
            for g2_term, match_index in list(g2_match.items()):
                if max(g2_match.values()) >= min_matching:
                    if (match_index == max(g2_match.values())) \
                            and not g2_term in g2_matched:
                        # Found matching term
                        g2_matched.add(g2_term)

                        if not g1_term == g2_term:
                            g2_name = graph2.qname(g2_term).split(":")[-1]
                            new_id = g1_term + '_' + g2_name
                            logging.debug(graph1.qname(g1_term) +
                                          " is matched to " +
                                          graph2.qname(g2_term) +
                                          " and replaced by " +
                                          graph2.qname(new_id) +
                                          " (match=" + str(match_index) + ")")

                            for p, o in graph1.predicate_objects(g1_term):
                                graph1.remove((g1_term, p, o))
                                graph1.add((new_id, p, o))
                            for p, o in graph2.predicate_objects(g2_term):
                                graph2.remove((g2_term, p, o))
                                graph2.add((new_id, p, o))
                            for s, p in graph1.subject_predicates(g1_term):
                                graph1.remove((s, p, g1_term))
                                graph1.add((s, p, new_id))
                            for s, p in graph2.subject_predicates(g2_term):
                                graph2.remove((s, p, g2_term))
                                graph2.add((s, p, new_id))

                            g2_terms.remove(g2_term)
                            g2_terms.add(new_id)
                        else:
                            logging.debug(graph1.qname(g1_term) +
                                          " is matched to " +
                                          graph2.qname(g2_term) +
                                          " (match=" + str(match_index) + ")")

                        match_found = True
                        break

            if not match_found:
                logging.debug("No match found for " + graph1.qname(g1_term))

        return list([graph1, graph2])

    def _reconcile_graphs(self, graph1, graph2, recursive=10):
        """
        Reconcile: if two entities have exactly the same attributes: they
        are considered to be the same (set the same id for both)
        """

        # FIXME: reconcile entities+agents first (ignoring non attributes)
        # then reconcile activities based on everything
        # for each item select the closest match in the other graph (instead of
            # perfect match)
        # this is needed to get sensible error messages when comparing graph
        # do not do recursive anymore

        # We reconcile first entities and agents (based on data properties) and
        # then activities (based on all relations)
        graph1, graph2 = self._replace_match(graph1, graph2, PROV['Entity'])
        graph1, graph2 = self._replace_match(graph1, graph2, PROV['Agent'])
        graph1, graph2 = self._replace_match(graph1, graph2, PROV['Activity'])

        return list([graph1, graph2])

    def compare_full_graphs(self, gt_graph, other_graph, owl, include=False,
                            raise_now=False):
        ''' Compare gt_graph and other_graph '''

        # We reconcile gt_graph with other_graph
        gt_graph, other_graph = self._reconcile_graphs(gt_graph, other_graph)

        gt_m_other = gt_graph - other_graph
        if not include:
            # Check for predicates which are not in common to both graphs (XOR)
            diff_graph = gt_graph ^ other_graph
        else:
            diff_graph = gt_m_other

        # FIXME: There is probably something better than using os.path.basename
        # to remove namespaces
        exlude = list()
        missing_s = list()

        exc_wrong = ""
        exc_wrong_literal = ""
        exc_added = ""
        exc_missing = ""

        for s, p, o in diff_graph.triples((None,  None, None)):
            # If triple is found in other_graph
            if (s,  p, o) in other_graph and (not p == NIDM_SOFTWARE_VERSION):
                # If subject is *not* found in gt_graph
                if (s,  None, None) not in gt_graph:
                    if not s in exlude:
                        if not isinstance(s, rdflib.term.BNode):
                            exc_added += "\nAdded s:\t'%s' should be removed" \
                                % (self.get_readable_name(owl, other_graph, s))
                            exlude.append(s)
                # If subject, predicate s, p is *not* found in gt_graph
                elif (s,  p, None) not in gt_graph:
                    if not p in exlude:
                        exc_added += "\nAdded p:\t'%s' should be removed" \
                            % (self.get_readable_name(owl, other_graph, p))
                        exlude.append(p)
                # If subject and predicate found in gt_graph, then object is
                # wrong (unless there is twice the same attribute and one value
                # is correct and the other wrong)
                # Alternatives are o_gt such as (s,p,o_gt) in gt and
                # (s,p,o_gt) *not* in other
                elif ((s,  p, None) in gt_graph):
                    if isinstance(o, rdflib.term.Literal):
                        same_json_array = False
                        close_float = False
                        same_str = False
                        for o_gt in gt_m_other.objects(s,  p):
                            same_json_array, close_float, same_str = \
                                self._same_json_or_float(o, o_gt)

                            if same_json_array or close_float or same_str:
                                # We found a match
                                break

                        if not same_json_array and not close_float and \
                                not same_str:
                            # Alternatives are o such as (s,p,o) in gt and
                            # (s,p,o) *not* in other
                            exc_wrong_literal += \
                                "\nWrong o:\t %s should be %s?" \
                                "\n\t\t ... in '%s %s %s'" \
                                % (
                                    self.get_readable_name(
                                        owl, other_graph, o),
                                    self.get_alternatives(
                                        owl, gt_m_other, s=s, p=p),
                                    self.get_readable_name(
                                        owl, other_graph, s),
                                    self.get_readable_name(
                                        owl, other_graph, p),
                                    self.get_readable_name(owl, other_graph, o)
                                )

                    elif not isinstance(o, rdflib.term.BNode):
                        exc_wrong += \
                            "\nWrong o:\t %s should be %s?" \
                            "\n\t\t ... in '%s %s %s'" \
                            % (
                                self.get_readable_name(owl, other_graph, o),
                                self.get_alternatives(owl, gt_graph, s=s, p=p),
                                self.get_readable_name(owl, other_graph, s),
                                self.get_readable_name(owl, other_graph, p),
                                self.get_readable_name(owl, other_graph, o)
                            )
                        # If object o is *not* found in gt_graph (and o is a
                        # URI, i.e. not the value of an attribute)
                elif (None,  None, o) not in gt_graph \
                        and isinstance(o, rdflib.term.URIRef):
                    if not o in exlude:
                        exc_added += "\nAdded o:\t'%s'" % (
                            self.get_readable_name(owl, other_graph, o))
                        exlude.append(o)
                # If subject and object found in gt_graph, then predicate is
                # wrong
                elif (s,  None, o) in gt_graph:
                    exc_wrong += "\nWrong p:\tBetween '%s' and '%s' " \
                                 "is '%s' (should be '%s'?)" \
                                 % (self.get_readable_name(
                                    owl, other_graph, s),
                                    self.get_readable_name(
                                        owl, other_graph, o),
                                    self.get_readable_name(
                                        owl, other_graph, p),
                                    self.get_alternatives(
                                        owl, gt_graph, s=s, o=o))
                # If predicate and object found in gt_graph, then subject is
                # wrong
                elif (None,  p, o) in gt_graph:
                    if not (s, None, None) in gt_graph:
                        if not s in exlude:
                            exc_added += "\nAdded:\t'%s'" % (s)
                            exlude.append(s)
                    else:
                        exc_wrong += "\nWrong s:\ts('%s') p('%s') o('%s')" \
                                     " not in gold std (should be s: '%s'?)" \
                                     % (self.get_readable_name(
                                        owl, other_graph, s),
                                        self.get_readable_name(
                                            owl, other_graph, p),
                                        self.get_readable_name(
                                            owl, other_graph, o),
                                        self.get_alternatives(
                                            owl, gt_graph, p=p, o=o))
                        # exc_wrong += "\nWrong s:\t'%s' \tto '%s' \tis '%s'
                        # (instead of %s)."%(os.path.basename(p),
                        # self.get_readable_name(owl, other_graph, o),
                        #  os.path.basename(s),found_subject)
                # If only subject found in gt_graph
                elif (s,  None, None) in gt_graph:
                    # gt_graph_possible_value = ""
                    # for (s_gt_graph,  p_gt_graph, o_gt_graph)
                    #  in gt_graph.triples((s,  p, None)):
                    #     gt_graph_possible_value += "; "+
                    # os.path.basename(p_gt_graph)
                    exc_added += "\nAdded:\tin '%s', '%s' \t ('%s')." \
                        % (self.get_readable_name(owl, gt_graph, s),
                           self.get_readable_name(owl, other_graph, p),
                           self.get_readable_name(owl, other_graph, o))
                else:
                    exc_added += "\nAdded:\tin '%s', '%s' \t ('%s')." \
                        % (self.get_readable_name(owl, gt_graph, s),
                           self.get_readable_name(owl, other_graph, p),
                           self.get_readable_name(owl, other_graph, o))

            # If subject and predicate are found in gt_graph
            elif (s,  p, o) in gt_graph and (not p == NIDM_SOFTWARE_VERSION):
                if (s,  p, None) in other_graph:
                    if isinstance(o, rdflib.term.Literal):
                        same_json_array = False
                        close_float = False

                        for o_gt in gt_graph.objects(s,  p):
                            same_json_array, close_float, same_str = \
                                self._same_json_or_float(o, o_gt)

                            if same_json_array or close_float or same_str:
                                # We found a match
                                break

                        if not same_json_array and not close_float and \
                                not same_str:
                            exc_wrong_literal += \
                                "\nWrong o:\t %s should be %s?" \
                                "\n\t\t ... in '%s %s %s'" \
                                % (
                                    self.get_alternatives(
                                        owl, other_graph, s=s, p=p),
                                    self.get_readable_name(owl, gt_graph, o),
                                    self.get_readable_name(
                                        owl, other_graph, s),
                                    self.get_readable_name(
                                        owl, other_graph, p),
                                    self.get_alternatives(
                                        owl, other_graph, s=s, p=p)
                                )

                        # exc_wrong_literal += "\nWrong literal o:\t p('%s') of
                        #  s('%s') is o(%s) but should be o(%s)." % (
                        #     self.get_readable_name(owl, other_graph, p),
                        #     self.get_readable_name(owl, other_graph, s),
                        #     self.get_alternatives(owl, other_graph, s=s,
                            # p=p),
                        #     self.get_readable_name(owl, gt_graph, o))
                    elif not isinstance(o, rdflib.term.BNode):
                        # Look for possible mimatched value (decide between
                        # wrong or missing)
                        wrong_o = list()
                        for o_alt in other_graph.objects(s,  p):
                            if (s, p, o_alt) not in gt_graph:
                                wrong_o.append(o_alt)

                        if wrong_o:
                            exc_wrong += "\nWrong o:\ts('%s') p('%s') o('%s') \
                            missing, o should be o(%s)?)" % (
                                self.get_readable_name(owl, other_graph, s),
                                self.get_readable_name(owl, other_graph, p),
                                self.get_alternatives(owl, other_graph, s=s, p=p),
                                self.get_readable_name(owl, gt_graph, o))
                        else:
                            exc_missing += "\nMissg o:\t %s is missing in %s?" \
                                "\n\t\t ... in %s %s %s'" \
                                % (
                                    self.get_readable_name(owl, gt_graph, o),
                                    self.get_readable_name(owl, gt_graph, s),
                                    self.get_readable_name(owl, gt_graph, s),
                                    self.get_readable_name(owl, gt_graph, p),
                                    self.get_readable_name(owl, gt_graph, o),
                                )
                        # If object o is *not* found in gt_graph (and o is a
                        # URI, i.e. not the value of an attribute)
                else:
                    #     if isinstance(o, rdflib.term.Literal):
                    #         if (not exc_wrong_literal):
                    #             exc_wrong_literal += "\nWrong literal o:\t
                    # p('%s') of s('%s') is ('%s') (instead o: '%s'?)"
                    # %(self.get_readable_name(owl, gt_graph, p),
                        # self.get_readable_name(owl, gt_graph, s),
                        # self.get_readable_name(owl, gt_graph, o),
                        # self.get_alternatives(owl, other_graph,s=s,p=p))
                    # else:
                    #     if (not exc_missing):
                    #         exc_missing += "\nMissing o (%s):\tp('%s')
                    # o('%s') \ton '%s'"%(type(o), self.get_readable_name(owl,
                        # gt_graph,
                    # p),self.get_readable_name(owl, gt_graph,o),
                    # self.get_readable_name(owl, gt_graph,s))
                    # If subject found in other_graph
                    if (s,  None, None) in other_graph:
                        exc_missing += "\nMissg p:\t %s is missing in %s?" \
                            "\n\t\t ... in %s %s %s'" \
                            % (
                                self.get_readable_name(owl, gt_graph, p),
                                self.get_readable_name(owl, gt_graph, s),
                                self.get_readable_name(owl, gt_graph, s),
                                self.get_readable_name(owl, gt_graph, p),
                                self.get_readable_name(owl, gt_graph, o),
                            )
                    # If subject is *not* found in other_graph
                    else:
                        if not s in missing_s:
                            if not isinstance(s, rdflib.term.BNode):
                                exc_missing += "\nMissg s:\t%s is missing " % (
                                    self.get_readable_name(owl, gt_graph, s))
                                missing_s.append(s)
            elif not p == NIDM_SOFTWARE_VERSION:
                exc_missing += "\nUNTRACKED ERROR"

        self.my_execption += exc_missing + \
            exc_added + exc_wrong + exc_wrong_literal

        if raise_now and self.my_execption:
            raise Exception(self.my_execption)

    def _same_json_or_float(self, o, o_other):
        # If string represents a json-array, then
        # compare as json data
        same_json_array = False
        if o.startswith("[") and o.endswith("]"):
            try:
                if json.loads(o) == json.loads(o_other):
                    same_json_array = True
            except ValueError:
                # Actually this string was not json
                same_json_array = False

        # If literal is a float allow for a small
        # tolerance to deal with possibly different
        # roundings
        close_float = False
        if o.datatype in [XSD.float, XSD.double]:
            if o_other.datatype in [XSD.float, XSD.double]:
                # If both are zero but of different type isclose returns false
                if o.value == 0 and o_other.value == 0:
                    close_float = True

                # Avoid None
                if o.value and o_other.value:
                    close_float = np.isclose(
                        o.value, o_other.value)

        same_str = False
        if o.datatype in [XSD.string, None]:
            if o_other.datatype in [XSD.string, None]:
                if o.value == o_other.value:
                    same_str = True

        return (same_json_array, close_float, same_str)


class ExampleGraph(object):
    '''Class representing a NIDM-Results examples graph to be compared to some
    ground truth graph'''

    def __init__(self, name, ttl_file, gt_ttl_files,
                 exact_comparison, version):
        self.name = name
        self.ttl_file = ttl_file

        self.gt_ttl_files = gt_ttl_files
        self.exact_comparison = exact_comparison
        self.graph = Graph()

        print(ttl_file)

        self.graph.parse(ttl_file, format='turtle')

        # Get NIDM-Results version for each example
        self.version = version

        if self.version != "dev":
            self.gt_ttl_files = [
                x.replace(os.path.join("nidm", "nidm"),
                          os.path.join("nidm_releases", self.version, "nidm"))
                for x in self.gt_ttl_files]

        # Owl file corresponding to version
        owl_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'owl',
            "nidm-results_" + version.replace(".", "") + ".owl")

        self.owl_file = owl_file

        owl_imports = None
        if self.version == "dev":
            owl_imports = glob.glob(
                os.path.join(os.path.dirname(owl_file),
                             os.pardir, os.pardir, "imports", '*.ttl'))
        self.owl = OwlReader(self.owl_file, owl_imports)
