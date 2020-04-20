from unittest import TestCase

from parse_2d import Diagram, SparseRegion
from parse_2d.tokens import TemplateTokenizer, Token, tokenize


class TestTemplateTokenizer(TestCase):
    @property
    def sample_diagram(self):
        return Diagram.from_string("abb\na bb")

    def test_template_tokenizer_starts_on(self):
        tokenizer = TemplateTokenizer({(0, 0): "b", (1, 1): "b"}, 1)

        self.assertTrue(tokenizer.starts_on("b"))
        self.assertFalse(tokenizer.starts_on("a"))

    def test_template_tokenizer_extract_token(self):
        b_obj = object()

        tokenizer = TemplateTokenizer({(0, 0): "b", (1, 1): "b"}, b_obj)
        token = Token(region=SparseRegion(frozenset([(1, 0), (2, 1)])), value=b_obj)

        self.assertEqual(
            token, tokenizer.extract_token(self.sample_diagram, (1, 0)),
        )
        self.assertEqual(
            token, tokenizer.extract_token(self.sample_diagram, (2, 1)),
        )

    def test_template_tokenizer_template_diagram(self):
        b_obj = object()

        tokenizer = TemplateTokenizer(Diagram.from_string("b\n b"), b_obj)

        self.assertEqual(
            Token(region=SparseRegion(frozenset([(2, 0), (3, 1)])), value=b_obj),
            tokenizer.extract_token(self.sample_diagram, (2, 0)),
        )

    def test_tokenize(self):
        a_obj = object()
        b_obj = object()

        tokenizers = [
            TemplateTokenizer(Diagram.from_string("a\na"), a_obj),
            TemplateTokenizer(Diagram.from_string("b\n b"), b_obj),
        ]

        self.assertEqual(
            [
                Token(
                    region=SparseRegion(contents=frozenset({(0, 0), (0, 1)})),
                    value=a_obj,
                ),
                Token(
                    region=SparseRegion(contents=frozenset({(1, 0), (2, 1)})),
                    value=b_obj,
                ),
                Token(
                    region=SparseRegion(contents=frozenset({(2, 0), (3, 1)})),
                    value=b_obj,
                ),
            ],
            list(tokenize(self.sample_diagram, tokenizers)),
        )
