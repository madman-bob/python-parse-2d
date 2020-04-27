from operator import and_, not_
from textwrap import dedent
from unittest import TestCase

from samples.circuit_diagram import (
    Circuit,
    Connection,
    ConnectionLabel,
    FuncNode,
    Function,
    InputNode,
    NodeInput,
    OpNode,
    OutputNode,
    parse_circuit_diagram,
)
from samples.circuit_diagram.parser.functions import (
    join_wires,
    split_wires,
    t,
    trim_wires,
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

    def test_circuit_diagram_wire_labels(self):
        tests = [
            (
                dedent(
                    """
                        -3-:
                    """
                ),
                frozenset({ConnectionLabel(constant=3)}),
            ),
            (
                dedent(
                    """
                        -12-:
                    """
                ),
                frozenset({ConnectionLabel(constant=12)}),
            ),
            (
                dedent(
                    """
                        -n+1-:
                    """
                ),
                frozenset({ConnectionLabel(constant=1, variables=("n",))}),
            ),
            (
                dedent(
                    """
                        -11+mn+qr+1-:
                    """
                ),
                frozenset({ConnectionLabel(constant=12, variables=("mn", "qr"))}),
            ),
            (
                dedent(
                    """
                        -12-m+n-:
                    """
                ),
                frozenset(
                    {
                        ConnectionLabel(constant=12),
                        ConnectionLabel(variables=("m", "n")),
                    }
                ),
            ),
            (
                dedent(
                    """
                        -.
                          1
                           2
                            .-:
                    """
                ),
                frozenset({ConnectionLabel(constant=12)}),
            ),
            (
                dedent(
                    """
                            .-:
                           2
                          1
                        -.
                    """
                ),
                frozenset({ConnectionLabel(constant=12)}),
            ),
            (
                dedent(
                    """
                        -.
                         1
                         2
                         .-:
                    """
                ),
                frozenset({ConnectionLabel(constant=12)}),
            ),
        ]

        for circuit_diagram, labels in tests:
            with self.subTest(circuit=circuit_diagram):
                self.assertEqual(
                    Circuit(
                        nodes={OutputNode(id=1), InputNode(id=0)},
                        connections={
                            Connection(
                                inputs=frozenset({0}),
                                outputs=frozenset({NodeInput(id=1, arg_pos=0)}),
                                labels=labels,
                            )
                        },
                    ),
                    parse_circuit_diagram(circuit_diagram),
                )

    def test_circuit_diagram_functions(self):
        tests = [
            (
                dedent(
                    """
                        -.
                          >-:
                        -.
                    """
                ),
                Circuit(
                    nodes={
                        InputNode(id=0),
                        InputNode(id=1),
                        OutputNode(id=2),
                        FuncNode(id=3, func=join_wires, arg_count=2, out_count=1),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({0}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({1}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=1)}),
                        ),
                        Connection(
                            inputs=frozenset({3}),
                            outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                        ),
                    },
                ),
            ),
            (
                dedent(
                    """
                           .:
                        --<
                           .:
                    """
                ),
                Circuit(
                    nodes={
                        InputNode(id=0),
                        OutputNode(id=1),
                        OutputNode(id=2),
                        FuncNode(id=3, func=split_wires, arg_count=1, out_count=2),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({0}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({3}),
                            outputs=frozenset({NodeInput(id=1, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({3}),
                            outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                        ),
                    },
                ),
            ),
            (
                dedent(
                    """
                        -.
                          %-:
                        -.
                    """
                ),
                Circuit(
                    nodes={
                        InputNode(id=0),
                        InputNode(id=1),
                        OutputNode(id=2),
                        FuncNode(id=3, func=trim_wires, arg_count=2, out_count=1),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({0}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({1}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=1)}),
                        ),
                        Connection(
                            inputs=frozenset({3}),
                            outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                        ),
                    },
                ),
            ),
            (
                dedent(
                    """
                        t-:
                    """
                ),
                Circuit(
                    nodes={
                        OutputNode(id=0),
                        FuncNode(id=1, func=t, arg_count=0, out_count=1),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({1}),
                            outputs=frozenset({NodeInput(id=0, arg_pos=0)}),
                        ),
                    },
                ),
            ),
        ]

        for circuit_diagram, circuit in tests:
            with self.subTest(circuit=circuit_diagram):
                self.assertEqual(
                    circuit, parse_circuit_diagram(circuit_diagram),
                )

    def test_circuit_diagram_user_functions(self):
        tests = [
            (
                dedent(
                    """
                        {*
                        --:
                        }

                        -*-:
                    """
                ),
                Circuit(
                    functions={
                        "*": Function(
                            name="*",
                            contents=Circuit(
                                nodes={InputNode(id=0), OutputNode(id=1)},
                                connections={
                                    Connection(
                                        inputs=frozenset({0}),
                                        outputs=frozenset({NodeInput(id=1, arg_pos=0)}),
                                    )
                                },
                            ),
                        )
                    },
                    nodes={
                        InputNode(id=0),
                        OutputNode(id=1),
                        FuncNode(id=2, func="*", arg_count=1, out_count=1),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({2}),
                            outputs=frozenset({NodeInput(id=1, arg_pos=0)}),
                        )
                    },
                ),
            ),
            (
                dedent(
                    """
                        {n00p
                        --:
                        }

                        -n00p-:
                    """
                ),
                Circuit(
                    functions={
                        "n00p": Function(
                            name="n00p",
                            contents=Circuit(
                                nodes={InputNode(id=0), OutputNode(id=1)},
                                connections={
                                    Connection(
                                        inputs=frozenset({0}),
                                        outputs=frozenset({NodeInput(id=1, arg_pos=0)}),
                                    )
                                },
                            ),
                        )
                    },
                    nodes={
                        InputNode(id=0),
                        OutputNode(id=1),
                        FuncNode(id=2, func="n00p", arg_count=1, out_count=1),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({2}),
                            outputs=frozenset({NodeInput(id=1, arg_pos=0)}),
                        )
                    },
                ),
            ),
            (
                dedent(
                    """
                        {*
                        -.
                          >-:
                        -.
                        }

                        -.
                          *-:
                        -.
                    """
                ),
                Circuit(
                    functions={
                        "*": Function(
                            name="*",
                            contents=Circuit(
                                nodes={
                                    InputNode(id=0),
                                    InputNode(id=1),
                                    OutputNode(id=2),
                                    FuncNode(
                                        id=3, func=join_wires, arg_count=2, out_count=1
                                    ),
                                },
                                connections={
                                    Connection(
                                        inputs=frozenset({0}),
                                        outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                                    ),
                                    Connection(
                                        inputs=frozenset({1}),
                                        outputs=frozenset({NodeInput(id=3, arg_pos=1)}),
                                    ),
                                    Connection(
                                        inputs=frozenset({3}),
                                        outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                                    ),
                                },
                            ),
                        )
                    },
                    nodes={
                        InputNode(id=0),
                        InputNode(id=1),
                        OutputNode(id=2),
                        FuncNode(id=3, func="*", arg_count=2, out_count=1),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({0}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({1}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=1)}),
                        ),
                        Connection(
                            inputs=frozenset({3}),
                            outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                        ),
                    },
                ),
            ),
            (
                dedent(
                    """
                        {*
                        -. .:
                          =
                        -. .:
                        }

                        -. .:
                          *
                        -. .:
                    """
                ),
                Circuit(
                    functions={
                        "*": Function(
                            name="*",
                            contents=Circuit(
                                nodes={
                                    InputNode(id=0),
                                    InputNode(id=1),
                                    OutputNode(id=2),
                                    OutputNode(id=3),
                                },
                                connections={
                                    Connection(
                                        inputs=frozenset({0}),
                                        outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                                    ),
                                    Connection(
                                        inputs=frozenset({1}),
                                        outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                                    ),
                                },
                            ),
                        )
                    },
                    nodes={
                        InputNode(id=0),
                        InputNode(id=1),
                        OutputNode(id=2),
                        OutputNode(id=3),
                        FuncNode(id=4, func="*", arg_count=2, out_count=2),
                    },
                    connections={
                        Connection(
                            inputs=frozenset({0}),
                            outputs=frozenset({NodeInput(id=4, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({1}),
                            outputs=frozenset({NodeInput(id=4, arg_pos=1)}),
                        ),
                        Connection(
                            inputs=frozenset({4}),
                            outputs=frozenset({NodeInput(id=2, arg_pos=0)}),
                        ),
                        Connection(
                            inputs=frozenset({4}),
                            outputs=frozenset({NodeInput(id=3, arg_pos=0)}),
                        ),
                    },
                ),
            ),
        ]

        for circuit_diagram, circuit in tests:
            with self.subTest(circuit=circuit_diagram):
                self.assertEqual(
                    circuit, parse_circuit_diagram(circuit_diagram),
                )
