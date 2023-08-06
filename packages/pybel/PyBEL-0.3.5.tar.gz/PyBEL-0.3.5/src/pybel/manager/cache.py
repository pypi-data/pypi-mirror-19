import itertools as itt
import logging

import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

from . import defaults
from . import models
from .utils import parse_owl, parse_datetime
from ..constants import DEFAULT_CACHE_LOCATION
from ..parser.language import value_map
from ..utils import download_url

log = logging.getLogger('pybel')

DEFAULT_BELNS_ENCODING = ''.join(sorted(value_map))


class BaseCacheManager:
    """Creates a connection to database and a persistient session using SQLAlchemy"""

    def __init__(self, connection=None, echo=False):
        self.connection = connection if connection is not None else 'sqlite:///' + DEFAULT_CACHE_LOCATION
        self.engine = create_engine(self.connection, echo=echo)
        self.sessionmaker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.sessionmaker)()
        self.create_database()

    def create_database(self, checkfirst=True):
        models.Base.metadata.create_all(self.engine, checkfirst=checkfirst)

    def drop_database(self):
        models.Base.metadata.drop_all(self.engine)


def extract_shared_required(config, definition_header='Namespace'):
    """

    :param config:
    :param definition_header: 'Namespace' or 'AnnotationDefinition'
    :return:
    """
    return {
        'keyword': config[definition_header]['Keyword'],
        'created': parse_datetime(config[definition_header]['CreatedDateTime']),
        'author': config['Author']['NameString'],
        'citation': config['Citation']['NameString']
    }


def extract_shared_optional(config, definition_header='Namespace'):
    s = {
        'description': (definition_header, 'DescriptionString'),
        'version': (definition_header, 'VersionString'),
        'license': ('Author', 'CopyrightString'),
        'contact': ('Author', 'ContactInfoString'),
        'citation_description': ('Citation', 'DescriptionString'),
        'citation_version': ('Citation', 'PublishedVersionString'),
        'citation_url': ('Citation', 'ReferenceURL')
    }

    x = {}

    for database_column, (section, key) in s.items():
        if section in config and key in config[section]:
            x[database_column] = config[section][key]

    if 'PublishedDate' in config['Citation']:
        x['citation_published'] = parse_datetime(config['Citation']['PublishedDate'])

    return x


class CacheManager(BaseCacheManager):
    def __init__(self, connection=None, echo=False):
        """The definition cache manager takes care of storing BEL namespace and annotation files for later use.
        It uses SQLite by default for speed and lightness, but any database can be used wiht its SQLAlchemy interface.

        :param connection: custom database connection string
        :type connection: str
        :param echo: Whether or not echo the running sql code.
        :type echo: bool
        """

        BaseCacheManager.__init__(self, connection=connection, echo=echo)

        self.namespace_cache = {}
        self.annotation_cache = {}

        self.term_cache = {}
        self.edge_cache = {}
        self.graph_cache = {}

    # NAMESPACE MANAGEMENT

    def insert_namespace(self, url):
        """Inserts the namespace file at the given location to the cache

        :param url: the location of the namespace file
        :type url: str
        :return: SQL Alchemy model instance, populated with data from URL
        :rtype: :class:`models.Namespace`
        """
        log.info('Caching namespace %s', url)

        config = download_url(url)

        namespace_insert_values = {
            'name': config['Namespace']['NameString'],
            'url': url,
            'domain': config['Namespace']['DomainString']
        }

        namespace_insert_values.update(extract_shared_required(config, 'Namespace'))
        namespace_insert_values.update(extract_shared_optional(config, 'Namespace'))

        namespace_mapping = {
            'species': ('Namespace', 'SpeciesString'),
            'query_url': ('Namespace', 'QueryValueURL')
        }

        for database_column, (section, key) in namespace_mapping.items():
            if section in config and key in config[section]:
                namespace_insert_values[database_column] = config[section][key]

        namespace = models.Namespace(**namespace_insert_values)

        values = {c: e if e else DEFAULT_BELNS_ENCODING for c, e in config['Values'].items() if c}

        namespace.entries = [models.NamespaceEntry(name=c, encoding=e) for c, e in values.items()]

        self.session.add(namespace)
        self.session.commit()

        return namespace

    def ensure_namespace(self, url):
        """Caches a namespace file if not already in the cache

        :param url: the location of the namespace file
        :type url: str
        """
        if url in self.namespace_cache:
            log.info('Already cached %s', url)
            return

        try:
            results = self.session.query(models.Namespace).filter(models.Namespace.url == url).one()
            log.info('Loaded namespace from %s (%d)', url, len(results.entries))
        except NoResultFound:
            results = self.insert_namespace(url)

        if results is None:
            raise ValueError('No results for {}'.format(url))
        elif not results.entries:
            raise ValueError('No entries for {}'.format(url))

        self.namespace_cache[url] = {entry.name: set(entry.encoding) for entry in results.entries}

    def get_namespace(self, url):
        """Returns a dict of names and their encodings for the given namespace file

        :param url: the location of the namespace file
        :type url: str
        """
        self.ensure_namespace(url)
        return self.namespace_cache[url]

    def ls_namespaces(self):
        """Returns a list of the locations of the stored namespaces and annotations"""
        return [definition.url for definition in self.session.query(models.Namespace).all()]

    def load_default_namespaces(self):
        """Caches the default set of namespaces"""
        for url in defaults.default_namespaces:
            self.ensure_namespace(url)

    # ANNOTATION MANAGEMENT

    def insert_annotation(self, url):
        """Inserts the namespace file at the given location to the cache

        :param url: the location of the namespace file
        :type url: str
        :return: SQL Alchemy model instance, populated with data from URL
        :rtype: :class:`models.Namespace`
        """
        log.info('Caching annotation %s', url)

        config = download_url(url)

        annotation_insert_values = {
            'type': config['AnnotationDefinition']['TypeString'],
            'url': url
        }
        annotation_insert_values.update(extract_shared_required(config, 'AnnotationDefinition'))
        annotation_insert_values.update(extract_shared_optional(config, 'AnnotationDefinition'))

        annotation_mapping = {
            'name': ('Citation', 'NameString')
        }

        for database_column, (section, key) in annotation_mapping.items():
            if section in config and key in config[section]:
                annotation_insert_values[database_column] = config[section][key]

        annotation = models.Annotation(**annotation_insert_values)
        annotation.entries = [models.AnnotationEntry(name=c, label=l) for c, l in config['Values'].items() if c]

        self.session.add(annotation)
        self.session.commit()

        return annotation

    def ensure_annotation(self, url):
        """Caches an annotation file if not already in the cache

        :param url: the location of the annotation file
        :type url: str
        """
        if url in self.annotation_cache:
            log.info('Already cached %s', url)
            return

        try:
            results = self.session.query(models.Annotation).filter(models.Annotation.url == url).one()
            log.info('Loaded annotation from %s (%d)', url, len(results.entries))
        except NoResultFound:
            results = self.insert_annotation(url)

        self.annotation_cache[url] = {entry.name: entry.label for entry in results.entries}

    def get_annotation(self, url):
        """Returns a dict of annotations and their labels for the given annotation file

        :param url: the location of the annotation file
        :type url: str
        """
        self.ensure_annotation(url)
        return self.annotation_cache[url]

    def ls_annotations(self):
        """Returns a list of the locations of the stored namespaces and annotations"""
        return [definition.url for definition in self.session.query(models.Annotation).all()]

    def load_default_annotations(self):
        """Caches the default set of annotations"""
        for url in defaults.default_annotations:
            self.ensure_annotation(url)

    # NAMESPACE OWL MANAGEMENT

    def insert_owl(self, iri):
        """Caches an ontology at the given IRI

        :param iri: the location of the ontology
        :type iri: str
        """
        log.info('Caching owl %s', iri)

        graph = parse_owl(iri)

        owl = models.Owl(iri=iri)

        entries = {node: models.OwlEntry(entry=node) for node in graph.nodes_iter()}

        owl.entries = list(entries.values())

        for u, v in graph.edges_iter():
            entries[u].children.append(entries[v])

        self.session.add(owl)
        self.session.commit()

        return owl

    def ensure_owl(self, iri):
        """Caches an ontology at the given IRI if it is not already in the cache

        :param iri: the location of the ontology
        :type iri: str
        """

        if iri in self.term_cache:
            return
        try:
            results = self.session.query(models.Owl).filter(models.Owl.iri == iri).one()
        except NoResultFound:
            results = self.insert_owl(iri)

        self.term_cache[iri] = set(entry.entry for entry in results.entries)
        self.edge_cache[iri] = set((sub.entry, sup.entry) for sub in results.entries for sup in sub.children)

        graph = nx.DiGraph()
        graph.add_edges_from(self.edge_cache[iri])
        self.graph_cache[iri] = graph

    def get_owl_terms(self, iri):
        """Gets a set of classes and individuals in the ontology at the given IRI

        :param iri: the location of the ontology
        :type iri: str
        """
        self.ensure_owl(iri)
        return self.term_cache[iri]

    def get_owl_edges(self, iri):
        """Gets a set of directed edge pairs from the graph representing the ontology at the given IRI

        :param iri: the location of the ontology
        :type iri: str
        """
        self.ensure_owl(iri)
        return self.edge_cache[iri]

    def get_owl_graph(self, iri):
        """Gets the graph representing the ontology at the given IRI

        :param iri: the location of the ontology
        :type iri: str
        """
        self.ensure_owl(iri)
        return self.graph_cache[iri]

    def ls_owl(self):
        """Returns a list of the locations of the stored ontologies"""
        return [owl.iri for owl in self.session.query(models.Owl).all()]

    def load_default_owl(self):
        """Caches the default set of ontologies"""
        for url in defaults.default_owl:
            self.ensure_owl(url)

    def ls(self):
        return itt.chain(self.ls_namespaces(), self.ls_annotations(), self.ls_owl())

    # Manage Equivalences

    def ensure_equivalence_class(self, label):
        try:
            result = self.session.query(models.NamespaceEntryEquivalence).filter_by(label=label).one()
        except NoResultFound:
            result = models.NamespaceEntryEquivalence(label=label)
            self.session.add(result)
            self.session.commit()
        return result

    def insert_equivalences(self, url, namespace_url):
        """Given a url to a .beleq file and its accompanying namespace url, populate the database"""
        self.ensure_namespace(namespace_url)

        log.info('Caching equivalences: %s', url)

        config = download_url(url)
        values = config['Values']

        ns = self.session.query(models.Namespace).filter_by(url=namespace_url).one()

        for entry in ns.entries:
            equivalence_label = values[entry.name]
            equivalence = self.ensure_equivalence_class(equivalence_label)
            entry.equivalence_id = equivalence.id

        ns.has_equivalences = True

        self.session.commit()

    def ensure_equivalences(self, url, namespace_url):
        """Check if the equivalence file is already loaded, and if not, load it"""
        self.ensure_namespace(namespace_url)

        ns = self.session.query(models.Namespace).filter_by(url=namespace_url).one()

        if not ns.has_equivalences:
            self.insert_equivalences(url, namespace_url)

    def get_equivalence_by_entry(self, namespace_url, name):
        """Gets the equivalence class

        :param namespace_url: the URL of the namespace
        :param name: the name of the entry in the namespace
        :return: the equivalence class of the entry in the given namespace
        """
        ns = self.session.query(models.Namespace).filter_by(url=namespace_url).one()
        ns_entry = self.session.query(models.NamespaceEntry).filter(models.NamespaceEntry.namespace_id == ns.id,
                                                                    models.NamespaceEntry.name == name).one()
        return ns_entry.equivalence

    def get_equivalence_members(self, equivalence_class):
        """Gets all members of the given equivalence class

        :param equivalence_class: the label of the equivalence class. example: '0b20937b-5eb4-4c04-8033-63b981decce7'
                                    for Alzheimer's Disease
        :return: a list of members of the class
        """
        eq = self.session.query(models.NamespaceEntryEquivalence).filter_by(label=equivalence_class).one()
        return eq.members
