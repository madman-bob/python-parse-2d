from unittest import TestCase

from parse_2d.diagram import Diagram


class TestDiagram(TestCase):
    @property
    def sample_diagram(self):
        return Diagram.from_string("abc\nd f\nghi")

    def test_diagram_get_index(self):
        self.assertEqual("b", self.sample_diagram[(1, 0)])

    def test_diagram_get_slice(self):
        self.assertEqual(
            Diagram.from_string("bc\n f"), self.sample_diagram[(1, 0):(3, 2)]
        )

    def test_diagram_set_index(self):
        diagram = self.sample_diagram
        diagram[(0, 1)] = "j"

        self.assertEqual("j", diagram[(0, 1)])

    def test_diagram_set_slice(self):
        diagram = self.sample_diagram
        diagram[(2, 0):(3, 3)] = Diagram.from_string("k\nl\nm")

        self.assertEqual(Diagram.from_string("bk\n l"), diagram[(1, 0):(3, 2)])

    def test_diagram_iter(self):
        self.assertEqual(
            [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2),],
            list(self.sample_diagram),
        )

    def test_diagram_len(self):
        self.assertEqual(8, len(self.sample_diagram))

    def test_diagram_contains(self):
        self.assertTrue((0, 0) in self.sample_diagram)
        self.assertFalse((1, 1) in self.sample_diagram)

    def test_diagram_keys(self):
        self.assertEqual(
            [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2),],
            list(self.sample_diagram),
        )

    def test_diagram_items(self):
        self.assertEqual(
            [
                ((0, 0), "a"),
                ((1, 0), "b"),
                ((2, 0), "c"),
                ((0, 1), "d"),
                ((2, 1), "f"),
                ((0, 2), "g"),
                ((1, 2), "h"),
                ((2, 2), "i"),
            ],
            list(self.sample_diagram.items()),
        )

    def test_diagram_values(self):
        self.assertEqual(
            list("abcdfghi"), list(self.sample_diagram.values()),
        )

    def test_diagram_get(self):
        diagram = self.sample_diagram
        sentinel = object()

        self.assertEqual("b", diagram.get((1, 0)))
        self.assertEqual("b", diagram.get((1, 0), sentinel))
        self.assertEqual(None, diagram.get((1, 1)))
        self.assertEqual(sentinel, diagram.get((1, 1), sentinel))
