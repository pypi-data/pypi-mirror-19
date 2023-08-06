import logging
import unittest

from pybel.constants import PYBEL_DEFAULT_NAMESPACE
from pybel.parser.parse_abundance_modifier import PmodParser, GmodParser, PsubParser, GsubParser, TruncParser, \
    FusionParser, LocationParser, FragmentParser
from pybel.parser.parse_abundance_modifier import VariantParser
from pybel.parser.parse_abundance_modifier import build_variant_dict, KIND, PMOD, GMOD, FRAGMENT

log = logging.getLogger(__name__)


class TestVariantParser(unittest.TestCase):
    def setUp(self):
        self.parser = VariantParser()

    def test_protein_del(self):
        statement = 'variant(p.Phe508del)'
        expected = build_variant_dict('p.Phe508del')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_protein_mut(self):
        statement = 'var(p.Gly576Ala)'
        expected = build_variant_dict('p.Gly576Ala')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_unspecified(self):
        statement = 'var(=)'
        expected = build_variant_dict('=')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_frameshift(self):
        statement = 'variant(p.Thr1220Lysfs)'
        expected = build_variant_dict('p.Thr1220Lysfs')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_snp(self):
        statement = 'var(delCTT)'
        expected = build_variant_dict('delCTT')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_chromosome_1(self):
        statement = 'variant(g.117199646_117199648delCTT)'
        expected = build_variant_dict('g.117199646_117199648delCTT')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_chromosome_2(self):
        statement = 'var(c.1521_1523delCTT)'
        expected = build_variant_dict('c.1521_1523delCTT')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_rna_del(self):
        statement = 'var(r.1653_1655delcuu)'
        expected = build_variant_dict('r.1653_1655delcuu')
        result = self.parser.parseString(statement)
        self.assertEqual(expected, result.asDict())

    def test_protein_trunc_triple(self):
        statement = 'var(p.Cys65*)'
        result = self.parser.parseString(statement)
        expected = build_variant_dict('p.Cys65*')
        self.assertEqual(expected, result.asDict())

    def test_protein_trunc_legacy(self):
        statement = 'var(p.65*)'
        result = self.parser.parseString(statement)
        expected = build_variant_dict('p.65*')
        self.assertEqual(expected, result.asDict())


class TestPmod(unittest.TestCase):
    def setUp(self):
        self.parser = PmodParser()

    def test_pmod1(self):
        statement = 'pmod(Ph, Ser, 473)'
        result = self.parser.parseString(statement)

        expected = {
            KIND: PMOD,
            PmodParser.IDENTIFIER: dict(namespace=PYBEL_DEFAULT_NAMESPACE, name='Ph'),
            PmodParser.CODE: 'Ser',
            PmodParser.POSITION: 473
        }
        self.assertEqual(expected, result.asDict())

    def test_pmod2(self):
        statement = 'pmod(Ph, Ser)'
        result = self.parser.parseString(statement)

        expected = {
            KIND: PMOD,
            PmodParser.IDENTIFIER: dict(namespace=PYBEL_DEFAULT_NAMESPACE, name='Ph'),
            PmodParser.CODE: 'Ser',
        }
        self.assertEqual(expected, result.asDict())

    def test_pmod3(self):
        statement = 'pmod(Ph)'
        result = self.parser.parseString(statement)

        expected = {
            KIND: PMOD,
            PmodParser.IDENTIFIER: dict(namespace=PYBEL_DEFAULT_NAMESPACE, name='Ph'),
        }
        self.assertEqual(expected, result.asDict())

    def test_pmod4(self):
        statement = 'pmod(P, S, 473)'
        result = self.parser.parseString(statement)

        expected = {
            KIND: PMOD,
            PmodParser.IDENTIFIER: dict(namespace=PYBEL_DEFAULT_NAMESPACE, name='Ph'),
            PmodParser.CODE: 'Ser',
            PmodParser.POSITION: 473
        }
        self.assertEqual(expected, result.asDict())

    def test_pmod5(self):
        statement = 'pmod(MOD:PhosRes, Ser, 473)'
        result = self.parser.parseString(statement)

        expected = {
            KIND: PMOD,
            PmodParser.IDENTIFIER: dict(namespace='MOD', name='PhosRes'),
            PmodParser.CODE: 'Ser',
            PmodParser.POSITION: 473
        }
        self.assertEqual(expected, result.asDict())


class TestGmod(unittest.TestCase):
    def setUp(self):
        self.parser = GmodParser()

        self.expected = {
            KIND: GMOD,
            GmodParser.IDENTIFIER: dict(namespace=PYBEL_DEFAULT_NAMESPACE, name='Me')
        }

    def test_gmod_short(self):
        statement = 'gmod(M)'
        result = self.parser.parseString(statement)
        self.assertEqual(self.expected, result.asDict())

    def test_gmod_unabbreviated(self):
        statement = 'gmod(Me)'
        result = self.parser.parseString(statement)
        self.assertEqual(self.expected, result.asDict())

    def test_gmod_long(self):
        statement = 'geneModification(methylation)'
        result = self.parser.parseString(statement)
        self.assertEqual(self.expected, result.asDict())


class TestPsub(unittest.TestCase):
    def setUp(self):
        self.parser = PsubParser()

    def test_psub_1(self):
        statement = 'sub(A, 127, Y)'
        result = self.parser.parseString(statement)

        expected_list = build_variant_dict('p.Ala127Tyr')
        self.assertEqual(expected_list, result.asDict())

    def test_psub_2(self):
        statement = 'sub(Ala, 127, Tyr)'
        result = self.parser.parseString(statement)

        expected_list = build_variant_dict('p.Ala127Tyr')
        self.assertEqual(expected_list, result.asDict())


class TestGsubParser(unittest.TestCase):
    def setUp(self):
        self.parser = GsubParser()

    def test_gsub(self):
        statement = 'sub(G,308,A)'
        result = self.parser.parseString(statement)

        expected_dict = build_variant_dict('g.308G>A')
        self.assertEqual(expected_dict, result.asDict())


class TestFragmentParser(unittest.TestCase):
    """See http://openbel.org/language/web/version_2.0/bel_specification_version_2.0.html#_examples_2"""

    def setUp(self):
        self.parser = FragmentParser()

    def test_known_length(self):
        """test known length"""
        s = 'frag(5_20)'
        result = self.parser.parseString(s)
        expected = {
            KIND: FRAGMENT,
            FragmentParser.START: 5,
            FragmentParser.STOP: 20
        }
        self.assertEqual(expected, result.asDict())

    def test_unknown_length(self):
        """amino-terminal fragment of unknown length"""
        s = 'frag(1_?)'
        result = self.parser.parseString(s)
        expected = {
            KIND: FRAGMENT,
            FragmentParser.START: 1,
            FragmentParser.STOP: '?'
        }
        self.assertEqual(expected, result.asDict())

    def test_unknown_start_stop(self):
        """fragment with unknown start/stop"""
        s = 'frag(?_*)'
        result = self.parser.parseString(s)
        expected = {
            KIND: FRAGMENT,
            FragmentParser.START: '?',
            FragmentParser.STOP: '*'
        }
        self.assertEqual(expected, result.asDict())

    def test_descriptor(self):
        """fragment with unknown start/stop and a descriptor"""
        s = 'frag(?, 55kD)'
        result = self.parser.parseString(s)
        expected = {
            KIND: FRAGMENT,
            FragmentParser.MISSING: '?',
            FragmentParser.DESCRIPTION: '55kD'
        }
        self.assertEqual(expected, result.asDict())


class TestTruncationParser(unittest.TestCase):
    def setUp(self):
        self.parser = TruncParser()

    def test_trunc_1(self):
        statement = 'trunc(40)'
        result = self.parser.parseString(statement)

        expected = build_variant_dict('p.40*')
        self.assertEqual(expected, result.asDict())


class TestFusionParser(unittest.TestCase):
    def setUp(self):
        self.parser = FusionParser()

    def test_261a(self):
        """RNA abundance of fusion with known breakpoints"""
        statement = 'fus(HGNC:TMPRSS2, r.1_79, HGNC:ERG, r.312_5034)'
        result = ['Fusion', ['HGNC', 'TMPRSS2'], ['r', 1, 79], ['HGNC', 'ERG'], ['r', 312, 5034]]
        self.assertEqual(result, self.parser.parseString(statement).asList())

    def test_261b(self):
        """RNA abundance of fusion with unspecified breakpoints"""
        statement = 'fus(HGNC:TMPRSS2, ?, HGNC:ERG, ?)'
        expected = ['Fusion', ['HGNC', 'TMPRSS2'], '?', ['HGNC', 'ERG'], '?']
        self.assertEqual(expected, self.parser.parseString(statement).asList())


class TestLocation(unittest.TestCase):
    def setUp(self):
        self.parser = LocationParser()

    def test_a(self):
        statement = 'loc(GOCC:intracellular)'
        result = self.parser.parseString(statement)
        expected = {
            'location': dict(namespace='GOCC', name='intracellular')
        }
        self.assertEqual(expected, result.asDict())
