from unittest import TestCase

from parse_2d import Diagram, RectRegion, Token
from parse_2d.tokens import BoxTokenizer, Directions


class TestBoxTokenizer(TestCase):
    @property
    def sample_diagram(self):
        return Diagram.from_string("┌──┐\n│ab│\n│cd│\n└──┘")

    @property
    def sample_box_tokenizer(self):
        return BoxTokenizer(
            {
                Directions.UP: frozenset({"─"}),
                Directions.UP_RIGHT: frozenset({"┐"}),
                Directions.RIGHT: frozenset({"│"}),
                Directions.DOWN_RIGHT: frozenset({"┘"}),
                Directions.DOWN: frozenset({"─"}),
                Directions.DOWN_LEFT: frozenset({"└"}),
                Directions.LEFT: frozenset({"│"}),
                Directions.UP_LEFT: frozenset({"┌"}),
            },
            lambda diagram: "\n".join(
                "".join(line[1:-1]) for line in diagram.contents[1:-1]
            ),
        )

    def test_box_tokenizer_starts_on(self):
        tokenizer = self.sample_box_tokenizer

        self.assertTrue(tokenizer.starts_on("│"))
        self.assertTrue(tokenizer.starts_on("┌"))
        self.assertFalse(tokenizer.starts_on("a"))

    def test_box_tokenizer_extract_token(self):
        tokenizer = self.sample_box_tokenizer
        token = Token(
            region=RectRegion(top_left=(0, 0), bottom_right=(4, 4)), value="ab\ncd"
        )

        self.assertEqual(token, tokenizer.extract_token(self.sample_diagram, (0, 0)))
        self.assertEqual(token, tokenizer.extract_token(self.sample_diagram, (1, 0)))
        self.assertEqual(token, tokenizer.extract_token(self.sample_diagram, (2, 3)))
        self.assertEqual(token, tokenizer.extract_token(self.sample_diagram, (3, 3)))
