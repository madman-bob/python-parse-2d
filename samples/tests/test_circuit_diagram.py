from operator import and_, not_
from textwrap import dedent
from unittest import TestCase

from samples.circuit_diagram import (
    Circuit,
    Connection,
    InputNode,
    NodeInput,
    OpNode,
    OutputNode,
    parse_circuit_diagram,
)


class TestCircuitDiagram(TestCase):
    def test_extract_circuit_diagram(self):
        circuit_diagram = dedent(
            """
                -.
                  a.:
                -.
            """
        )

        circuit = Circuit(
            nodes={
                InputNode(id=0),
                InputNode(id=1),
                OutputNode(id=2),
                OpNode(id=3, func=and_, arg_count=2),
            },
            connections={
                Connection(
                    inputs=frozenset({0}), outputs=frozenset({NodeInput(3, 0)}),
                ),
                Connection(
                    inputs=frozenset({1}), outputs=frozenset({NodeInput(3, 1)}),
                ),
                Connection(
                    inputs=frozenset({3}), outputs=frozenset({NodeInput(2, 0)}),
                ),
            },
        )

        with self.subTest("Parse"):
            self.assertEqual(
                circuit, parse_circuit_diagram(circuit_diagram),
            )

    def test_extract_circuit_diagram_flip_flop(self):
        circuit_diagram = dedent(
            """
                --.~.
                   =
                  .~.--:
            """
        )

        circuit = Circuit(
            nodes={
                InputNode(id=0),
                OutputNode(id=1),
                OpNode(id=2, func=not_, arg_count=1),
                OpNode(id=3, func=not_, arg_count=1),
            },
            connections={
                Connection(
                    inputs=frozenset({0, 3}),
                    outputs=frozenset({NodeInput(1, 0), NodeInput(2, 0)}),
                ),
                Connection(inputs=frozenset({2}), outputs=frozenset({NodeInput(3, 0)})),
            },
        )

        with self.subTest("Parse"):
            self.assertEqual(
                circuit, parse_circuit_diagram(circuit_diagram),
            )

    def test_circuit_diagram_io_non_interference(self):
        circuit_diagram = dedent(
            """
                --:
                -.:
                --:
            """
        )

        circuit = Circuit(
            nodes={
                InputNode(id=0),
                InputNode(id=1),
                InputNode(id=2),
                OutputNode(id=3),
                OutputNode(id=4),
                OutputNode(id=5),
            },
            connections={
                Connection(inputs=frozenset({0}), outputs=frozenset({NodeInput(3, 0)})),
                Connection(inputs=frozenset({1}), outputs=frozenset({NodeInput(4, 0)})),
                Connection(inputs=frozenset({2}), outputs=frozenset({NodeInput(5, 0)})),
            },
        )

        with self.subTest("Parse"):
            self.assertEqual(
                circuit, parse_circuit_diagram(circuit_diagram),
            )
