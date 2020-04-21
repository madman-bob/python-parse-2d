from unittest import TestCase

from parse_2d import Diagram
from parse_2d.tokens import Directions, Token, Wire, WireSocket, WireTokenizer


class TestWireTokenizer(TestCase):
    @property
    def sample_diagram(self):
        return Diagram.from_string("a─┐\n  └──b")

    def test_wire_tokenizer_starts_on(self):
        tokenizer = WireTokenizer(
            {
                "─": Directions.horizontal,
                "┐": {Directions.LEFT.value, Directions.DOWN.value},
                "└": {Directions.UP.value, Directions.RIGHT.value},
            }
        )

        self.assertTrue(tokenizer.starts_on("─"))
        self.assertTrue(tokenizer.starts_on("┐"))
        self.assertTrue(tokenizer.starts_on("└"))
        self.assertFalse(tokenizer.starts_on("a"))
        self.assertFalse(tokenizer.starts_on("b"))

    def test_wire_tokenizer_extract_token(self):
        tokenizer = WireTokenizer(
            {
                "─": Directions.horizontal,
                "┐": {Directions.LEFT.value, Directions.DOWN.value},
                "└": {Directions.UP.value, Directions.RIGHT.value},
            }
        )

        token = Token(
            region={(1, 0), (2, 0), (2, 1), (3, 1), (4, 1)},
            value=Wire(
                sockets=frozenset(
                    {
                        WireSocket(location=(0, 0), direction=Directions.RIGHT.value),
                        WireSocket(location=(5, 1), direction=Directions.LEFT.value),
                    }
                )
            ),
        )

        self.assertEqual(
            token, tokenizer.extract_token(self.sample_diagram, (1, 0)),
        )
        self.assertEqual(
            token, tokenizer.extract_token(self.sample_diagram, (2, 1)),
        )

    def test_wire_tokenizer_wire_loop(self):
        diagram = Diagram.from_string("┌─┐\n└─┘")

        tokenizer = WireTokenizer(
            {
                "─": Directions.horizontal,
                "┌": {Directions.DOWN.value, Directions.RIGHT.value},
                "┐": {Directions.LEFT.value, Directions.DOWN.value},
                "└": {Directions.UP.value, Directions.RIGHT.value},
                "┘": {Directions.LEFT.value, Directions.UP.value},
            }
        )

        self.assertEqual(
            Token(
                region={(0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)},
                value=Wire(sockets=frozenset()),
            ),
            tokenizer.extract_token(diagram, (0, 0)),
        )

    def test_wire_tokenizer_custom_outgoing_directions(self):
        class MirrorWireTokenizer(WireTokenizer[str]):
            """
            Wire tokenizer that uses `/` as though it were a mirror,
            bouncing incoming signals off in complementary directions
            """

            def connections(self, segment, incoming_direction=None):
                if segment == "/" and incoming_direction is not None:
                    return {
                        {
                            Directions.UP.value: Directions.LEFT.value,
                            Directions.RIGHT.value: Directions.DOWN.value,
                            Directions.DOWN.value: Directions.RIGHT.value,
                            Directions.LEFT.value: Directions.UP.value,
                        }[incoming_direction]
                    }

                return super().connections(segment, incoming_direction)

        tokenizer = MirrorWireTokenizer(
            {
                "┌": {Directions.DOWN.value, Directions.RIGHT.value},
                "┐": {Directions.LEFT.value, Directions.DOWN.value},
                "└": {Directions.UP.value, Directions.RIGHT.value},
                "┘": {Directions.LEFT.value, Directions.UP.value},
                "/": Directions.horizontal + Directions.vertical,
            }
        )

        with self.subTest("Figure 8 diagram"):
            figure_8_diagram = Diagram.from_string(" ┌┐\n┌/┘\n└┘")

            figure_8_token = Token(
                region={(1, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2), (0, 1)},
                value=Wire(sockets=frozenset()),
            )

            self.assertEqual(
                figure_8_token, tokenizer.extract_token(figure_8_diagram, (1, 0))
            )

        with self.subTest("Two squares diagram"):
            two_squares_diagram = Diagram.from_string("┌┐\n└/┐\n └┘")

            upper_square_token = Token(
                region={(0, 0), (0, 1), (1, 1), (1, 0)}, value=Wire(sockets=frozenset())
            )
            lower_square_token = Token(
                region={(2, 2), (1, 2), (1, 1), (2, 1)}, value=Wire(sockets=frozenset())
            )

            self.assertEqual(
                upper_square_token, tokenizer.extract_token(two_squares_diagram, (0, 0))
            )
            self.assertEqual(
                lower_square_token, tokenizer.extract_token(two_squares_diagram, (2, 2))
            )
