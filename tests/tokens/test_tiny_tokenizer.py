from unittest import TestCase

from parse_2d import Diagram, TinyRegion
from parse_2d.tokens import TinyTokenizer, Token, tokenize


class TestTinyTokenizer(TestCase):
    @property
    def sample_diagram(self):
        return Diagram.from_string("a b\nba")

    def test_tiny_tokenizer_starts_on(self):
        tokenizer = TinyTokenizer("b", 1)

        self.assertTrue(tokenizer.starts_on("b"))
        self.assertFalse(tokenizer.starts_on("a"))

    def test_tiny_tokenizer_extract_token(self):
        b_obj = object()

        tokenizer = TinyTokenizer("b", b_obj)

        self.assertEqual(
            Token(region=TinyRegion(location=(0, 1)), value=b_obj),
            tokenizer.extract_token(self.sample_diagram, (0, 1)),
        )

    def test_tokenize(self):
        a_obj = object()
        b_obj = object()

        tokenizers = [
            TinyTokenizer("a", a_obj),
            TinyTokenizer("b", b_obj),
        ]

        self.assertEqual(
            [
                Token(region=TinyRegion(location=(0, 0)), value=a_obj),
                Token(region=TinyRegion(location=(2, 0)), value=b_obj),
                Token(region=TinyRegion(location=(0, 1)), value=b_obj),
                Token(region=TinyRegion(location=(1, 1)), value=a_obj),
            ],
            list(tokenize(self.sample_diagram, tokenizers)),
        )
