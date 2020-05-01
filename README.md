# parse_2d

Tools for parsing two-dimensional programming languages.

## Example

Suppose we want to parse a diagram representing a path, with `>`, `v`, `<`, and `^` each being single steps.

```
>v  >>
 v  ^
 >>>^
```

One way of tokenizing this is to interpret each of these steps as a token, with a value representing its direction.

```python
from parse_2d import Diagram, TinyTokenizer, tokenize

diagram = Diagram.from_string(">v  >>\n v  ^\n >>>^")

tokenizers = [
    TinyTokenizer(">", 0),
    TinyTokenizer("v", 1),
    TinyTokenizer("<", 2),
    TinyTokenizer("^", 3),
]

for token in tokenize(diagram, tokenizers):
    print(token)
```

Each `Token` has a region and a value. The region is what area it covers in the original diagram, while the value can be any Python object representing what you've tokenized.

Alternatively, you can extract the path as a single token, using the `WireTokenizer`, or as a directed path, by subclassing `WireTokenizer`.

A more complete [sample](https://github.com/madman-bob/python-parse-2d/tree/master/samples/circuit_diagram) is also provided, to demonstrate the use of these tools, by parsing the [Circuit Diagram](https://esolangs.org/wiki/Circuit_Diagram) language.

## Reference

### `Diagram`

A `Diagram` is an infinite two-dimensional grid of "symbols", with a distinguished "whitespace" symbol. `Diagram`s may be instantiated with a list of lists and the whitespace symbol, or by the `from_string` method.

#### Manual instantiation

```pycon
>>> diagram = Diagram([[1, 2], [3]], 0)
>>> diagram[(0, 1)]
3
>>> diagram[(1, 1)]
0
>>> diagram[(-30, 17)]
0
```

#### `from_string`

```pycon
>>> diagram = Diagram.from_string("ab\nc")
>>> diagram[(0, 1)]
'c'
>>> diagram[(1, 1)]
' '
```

### `Region`

A `Region` is an area on a diagram. Custom `Region`s may be made by inheriting from `Region`. The following `Region`s are provided by default:

#### `TinyRegion(location)`

A `Region` consisting of a single point. Has the `location` property to provide that point.

#### `RectRegion(top_left, bottom_right)`

A rectangular `Region`, aligned with the axes, consisting of the points bounded by `top_left` and `bottom_right`, including the top and left edges, and excluding the bottom and right edges (analogously to `range`).

#### `SparseRegion(contents)`

A `Region` consisting of a collection of disparate points. Has the `contents` property to provide that `frozenset` of points.

### `Token`

A `Token` consists of a `region` covered, and a `value` that the token represents.

### `Tokenizer`

A `Tokenizer` is an object for extracting tokens from diagrams. Custom `Tokenizer` classes may be made by inheriting from `Tokenizer`, and overriding the `starts_on` and `extract_token` methods. See the `Tokenizer` docstring for more details.

#### `TinyTokenizer(symbol, value)`

Tokenizer for tokens represented by a single symbol.

Extracts a token of value `token_value` for every `symbol` in the diagram.

#### `TemplateTokenizer(template, token_value)`

Tokenizer for tokens represented by a fixed template of symbols.

The `template` is either a mapping of relative locations to symbols, or a `Diagram`.

Extracts a token of value `token_value` for every non-overlapping translation of the template found in the parent Diagram.

#### `WireTokenizer(segment_connections)`

Tokenizer for wire tokens, represented by a path through a diagram.

A wire consists of multiple symbol "segments", each of which has a fixed collection of directions it can connect to.

The `segment_connections` is a mapping from segment symbols to a collection of that segment's available connections.

Extracts a wire token representing the available connections to that wire.

This class assumes that segments connect all possible incoming directions to all possible outgoing directions. Child classes may override this behavior by overriding the `connections` method. See the `WireTokenizer` docstring for more details.

#### `BoxTokenizer(edge_symbols, contents_tokenizer)`

Tokenizer for tokens represented by a box of edge symbols.

`edge_tokens` is a mapping from a side of the box, to the collection of symbols that may be used for that edge.

`contents_tokenizer` is a function to determine the value of the extracted token, and is passed the entire box (including the edge) as its only parameter.

### `tokenize(diagram, tokenizers)`

Yields the non-overlapping tokens found in the `diagram` by the list of `tokenizers`.

## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install parse_2d
```
