from unittest import TestCase

from parse_2d.regions import RectRegion, SparseRegion, TinyRegion


class TestRegions(TestCase):
    def test_tiny_region(self):
        region = TinyRegion((0, 0))

        self.assertIn((0, 0), region)
        self.assertNotIn((0, 1), region)

        self.assertEqual([(0, 0)], list(region))
        self.assertEqual(1, len(region))

    def test_rect_region(self):
        region = RectRegion((0, 0), (2, 3))

        self.assertIn((0, 0), region)
        self.assertIn((1, 1), region)
        self.assertIn((1, 2), region)

        self.assertNotIn((2, 2), region)
        self.assertNotIn((-1, 0), region)

        self.assertEqual([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)], list(region))
        self.assertEqual(6, len(region))

    def test_sparse_region(self):
        elements = frozenset([(0, 0), (1, 1), (2, 3)])
        region = SparseRegion(elements)

        self.assertIn((0, 0), region)
        self.assertIn((1, 1), region)
        self.assertIn((2, 3), region)

        self.assertNotIn((1, 0), region)
        self.assertNotIn((0, 1), region)
        self.assertNotIn((2, 2), region)

        self.assertEqual(elements, frozenset(list(region)))
        self.assertEqual(3, len(region))
