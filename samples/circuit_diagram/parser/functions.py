from datetime import datetime
from typing import Callable, Dict, Iterable, Iterator, List

from parse_2d import Diagram, Index, TemplateTokenizer, tokenize
from samples.circuit_diagram.ast import (
    Circuit,
    FuncNode,
    Function,
    InputNode,
    OutputNode,
)

__all__ = [
    "split_wires",
    "join_wires",
    "trim_wires",
    "t",
    "parse_function_defs",
    "parse_functions",
]


def int_to_signal(n: int, wire_count: int) -> List[bool]:
    return [bool(n >> i & 1) for i in range(wire_count - 1, -1, -1)]


split_wires = lambda a: [a[: len(a) // 2], a[len(a) // 2 :]]
join_wires = lambda a, b: [a + b]
trim_wires = lambda a, b: [b[len(a) :]]
t = lambda: [
    int_to_signal(int((datetime.now() - datetime(2000, 1, 1)).total_seconds()), 32)
]

function_tokenizers = [
    TemplateTokenizer(Diagram.from_string("<"), (split_wires, 1, 2)),
    TemplateTokenizer(Diagram.from_string(">"), (join_wires, 2, 1)),
    TemplateTokenizer(Diagram.from_string("%"), (trim_wires, 2, 1)),
    TemplateTokenizer(Diagram.from_string("t"), (t, 0, 1)),
]


def user_function_tokenizer(function):
    arg_count = sum(
        1 for node in function.contents.nodes if isinstance(node, InputNode)
    )
    out_count = sum(
        1 for node in function.contents.nodes if isinstance(node, OutputNode)
    )

    return TemplateTokenizer(
        Diagram.from_string(function.name), (function.name, arg_count, out_count)
    )


def parse_function_defs(
    diagram: Diagram[str], parse_function_contents: Callable[[Diagram[str]], Circuit]
) -> Iterator[Function]:
    y_start = None

    for y in range(len(diagram.contents)):
        if diagram[(0, y)] == "{":
            y_start = y
        elif diagram[(0, y)] == "}":
            y_end = y

            yield Function(
                "".join(diagram.contents[y_start][1:]),
                parse_function_contents(
                    Diagram(diagram.contents[y_start + 1 : y_end], diagram.whitespace)
                ),
            )

            diagram.contents[y_start : y_end + 1] = [
                [] for _ in range(y_end - y_start + 1)
            ]


def parse_functions(
    diagram: Diagram[str], node_ids: Iterator[int], user_functions: Iterable[Function]
) -> Dict[Index, FuncNode]:
    user_function_tokenizers = [
        user_function_tokenizer(function) for function in user_functions
    ]

    functions_by_region = {
        token.region: FuncNode(next(node_ids), *token.value)
        for token in tokenize(diagram, function_tokenizers + user_function_tokenizers)
    }

    functions_by_index = {
        i: node for region, node in functions_by_region.items() for i in region
    }

    for function_index in functions_by_index:
        diagram[function_index] = "#function"

    return functions_by_index
