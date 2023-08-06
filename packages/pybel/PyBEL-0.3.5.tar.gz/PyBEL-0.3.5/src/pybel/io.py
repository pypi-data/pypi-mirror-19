# -*- coding: utf-8 -*-

import codecs
import json
import logging
import os
from ast import literal_eval

import networkx as nx
import py2neo
import requests
from networkx import GraphMLReader
from networkx.readwrite import json_graph
from requests_file import FileAdapter

from .canonicalize import decanonicalize_node
from .constants import PYBEL_CONTEXT_TAG, FUNCTION, NAME, RELATION
from .graph import BELGraph, expand_edges, GRAPH_ANNOTATION_LIST
from .utils import flatten, flatten_graph_data

try:
    import cPickle as pickle
except ImportError:
    import pickle

__all__ = [
    'from_lines',
    'from_path',
    'from_url',
    'to_pickle',
    'to_bytes',
    'from_bytes',
    'from_pickle',
    'to_json',
    'from_json',
    'to_graphml',
    'from_graphml',
    'to_csv',
    'to_neo4j'
]

log = logging.getLogger('pybel')


def from_lines(lines, **kwargs):
    """Loads a BEL graph from an iterable over the lines of a BEL script. This can be a list of strings, file, or other.
    This function is a *very* thin wrapper around :py:meth:`BELGraph`.

    :param lines: an iterable of strings (the lines in a BEL script)
    :type lines: iter
    :param kwargs: keyword arguments to pass to :py:meth:`BELGraph`
    :return: a parsed BEL graph
    :rtype: :class:`BELGraph`
    """
    return BELGraph(lines=lines, **kwargs)


def from_path(path, encoding='utf-8', **kwargs):
    """Loads a BEL graph from a file resource

    :param path: a file path
    :type path: str
    :param encoding: the encoding to use when reading this file. Is passed to codecs.open.
                     See https://docs.python.org/3/library/codecs.html#standard-encodings for a list of standard
                     encodings. For example, files starting with a UTF-8 BOM should use 'utf_8_sig'
    :type encoding: str
    :param kwargs: keyword arguments to pass to :py:meth:`BELGraph`
    :return: a parsed BEL graph
    :rtype: :class:`BELGraph`
    """
    log.info('Loading from path: %s', path)
    with codecs.open(os.path.expanduser(path), encoding=encoding) as f:
        return BELGraph(lines=f, **kwargs)


def from_url(url, **kwargs):
    """Loads a BEL graph from a URL resource

    :param url: a valid URL pointing to a BEL resource
    :type url: str
    :param kwargs: keyword arguments to pass to :py:meth:`BELGraph`
    :return: a parsed BEL graph
    :rtype: :class:`BELGraph`
    """
    log.info('Loading from url: %s', url)

    session = requests.session()
    session.mount('file://', FileAdapter())

    response = session.get(url)
    response.raise_for_status()

    lines = (line.decode('utf-8') for line in response.iter_lines())

    return BELGraph(lines=lines, **kwargs)


def to_bytes(graph, protocol=pickle.HIGHEST_PROTOCOL):
    """Converts a graph to bytes (as BytesIO object)

    :param graph: a BEL graph
    :type graph: BELGraph
    :param protocol: Pickling protocol to use
    :type protocol: int
    :rtype: bytes
    """
    return pickle.dumps(graph, protocol=protocol)


def from_bytes(bytes_graph):
    """Reads a graph from bytes (BytesIO objet)

    :param bytes_graph: File or filename to write
    :type bytes_graph: bytes
    :rtype: :class:`BELGraph`
    """
    return pickle.loads(bytes_graph)


def to_pickle(graph, output, protocol=pickle.HIGHEST_PROTOCOL):
    """Writes this graph to a pickle object with nx.write_gpickle

    Cast as a nx.MultiDiGraph before outputting because the pickle serializer can't handle the PyParsing elements
    within the BELGraph class.

    :param graph: a BEL graph
    :type graph: BELGraph
    :param output: a file or filename to write to
    :type output: file or file-like
    :param protocol: Pickling protocol to use
    :type protocol: int
    """
    nx.write_gpickle(graph, output, protocol=protocol)


def from_pickle(path):
    """Reads a graph from a gpickle file

    :param path: File or filename to read. Filenames ending in .gz or .bz2 will be uncompressed.
    :type path: file or str
    :rtype: :class:`BELGraph`
    """
    return nx.read_gpickle(path)


def to_json(graph, output):
    """Writes this graph to a node-link JSON object

    :param graph: a BEL graph
    :type graph: BELGraph
    :param output: a write-supporting file-like object
    """
    data = json_graph.node_link_data(graph)
    data['graph']['annotation_list'] = {k: list(sorted(v)) for k, v in data['graph'][GRAPH_ANNOTATION_LIST].items()}
    json.dump(data, output, ensure_ascii=False)


def from_json(path):
    """Reads graph from node-link JSON Object

    :param path: file path to read
    :type path: str
    :rtype: :class:`BELGraph`
    """
    with open(os.path.expanduser(path)) as f:
        data = json.load(f)

    for i, node in enumerate(data['nodes']):
        data['nodes'][i]['id'] = tuple(node['id'])

    g = json_graph.node_link_graph(data, directed=True, multigraph=True)
    return BELGraph(data=g)


def to_graphml(graph, output):
    """Writes this graph to GraphML file. Use .graphml extension so Cytoscape can recognize it

    :param graph: a BEL graph
    :type graph: BELGraph
    :param output: a file or filelike object
    """
    g = nx.MultiDiGraph()

    for node, data in graph.nodes(data=True):
        g.add_node(node, json=json.dumps(data))

    for u, v, key, data in graph.edges(data=True, keys=True):
        g.add_edge(u, v, key=key, attr_dict=flatten(data))

    nx.write_graphml(g, output)


def from_graphml(path):
    """Reads a graph from a graphml file

    :param path: File or filename to write
    :type path: file or str
    :rtype: :class:`BELGraph`
    """
    reader = GraphMLReader(node_type=str)
    reader.multigraph = True
    g = list(reader(path=path))[0]
    g = expand_edges(g)
    for n in g.nodes_iter():
        g.node[n] = json.loads(g.node[n]['json'])
    nx.relabel_nodes(g, literal_eval, copy=False)  # shh don't tell anyone
    return BELGraph(data=g)


def to_csv(graph, output):
    """Writes graph to edge list csv

    :param graph: a BEL graph
    :type graph: BELGraph
    :param output: a file or filelike object
    """
    nx.write_edgelist(flatten_graph_data(graph), output, data=True)


def to_neo4j(graph, neo_graph, context=None):
    """Uploads a BEL graph to Neo4J graph database using `py2neo`

    :param graph: a BEL Graph
    :type graph: BELGraph
    :param neo_graph: a py2neo graph object, Refer to the
                        `py2neo documentation <http://py2neo.org/v3/database.html#the-graph>`_
                        for how to build this object.
    :type neo_graph: :class:`py2neo.Graph`
    :param context: a disease context to allow for multiple disease models in one neo4j instance.
                    Each edge will be assigned an attribute :code:`pybel_context` with this value
    :type context: str
    """
    tx = neo_graph.begin()

    node_map = {}
    for node, data in graph.nodes(data=True):
        node_type = data[FUNCTION]
        attrs = {k: v for k, v in data.items() if k != FUNCTION}

        if NAME in data:
            attrs['value'] = data[NAME]

        node_map[node] = py2neo.Node(node_type, bel=decanonicalize_node(graph, node), **attrs)

        tx.create(node_map[node])

    for u, v, data in graph.edges(data=True):
        neo_u = node_map[u]
        neo_v = node_map[v]
        rel_type = data[RELATION]
        attrs = flatten(data)
        if context is not None:
            attrs[PYBEL_CONTEXT_TAG] = str(context)
        rel = py2neo.Relationship(neo_u, rel_type, neo_v, **attrs)
        tx.create(rel)

    tx.commit()
