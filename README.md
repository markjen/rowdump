# RowDump

A modern, structured, no-dependency Python library for formatted table output
with support for custom formatting, ASCII box drawing, and flexible column
definitions.

## Features

- **Structured table output** with customizable column definitions
- **ASCII box drawing** for beautiful table borders
- **Header separators** with optional line between header and data
- **Custom formatters** for data transformation
- **Automatic text truncation** with configurable suffixes
- **DateTime formatting** with RFC3339 support
- **Custom delimiters** and output functions
- **Empty value handling** with custom placeholders
- **Multiple table support** with automatic table management

## Installation

```bash
pip install rowdump
```

**Requirements:** Python 3.10+

## Quick Start

```python
from datetime import datetime
from rowdump import Column, Dump

# Create a dump instance
dump = Dump()

# Define columns
columns = [
    Column("id", "ID", int, 5),
    Column("name", "Name", str, 15),
    Column("age", "Age", int, 3),
    Column("city", "City", str, 12),
]

# Set columns and print header
dump.cols(columns)

# Add rows
dump.row({"id": 1, "name": "Alice", "age": 30, "city": "New York"})
dump.row({"id": 2, "name": "Bob", "age": 25, "city": "San Francisco"})
dump.row({"id": 3, "name": "Charlie", "age": 35, "city": "Los Angeles"})

# Close table and print summary
dump.close()
```

Output:
```
ID    Name            Age City        
1     Alice           30  New York    
2     Bob             25  San Franc...
3     Charlie         35  Los Angeles 
Total rows: 3
```

## ASCII Box Formatting

```python
dump = Dump(ascii_box=True)

columns = [
    Column("product", "Product", str, 20),
    Column("price", "Price", float, 10),
    Column("stock", "Stock", int, 8),
]

dump.cols(columns)
dump.row({"product": "Laptop", "price": 999.99, "stock": 15})
dump.row({"product": "Mouse", "price": 25.50, "stock": 100})
dump.close()
```

Output:
```
┌────────────────────┬──────────┬────────┐
│Product             │Price     │Stock   │
├────────────────────┼──────────┼────────┤
│Laptop              │999.99    │15      │
│Mouse               │25.5      │100     │
└────────────────────┴──────────┴────────┘
Total rows: 2
```

## Custom Formatters

```python
def currency_formatter(value):
    if value is None:
        return "$0.00"
    return f"${value:.2f}"

dump = Dump(ascii_box=True)

columns = [
    Column("item", "Item", str, 12),
    Column("price", "Price", float, 10, formatter=currency_formatter),
    Column("quantity", "Qty", int, 5),
]

dump.cols(columns)
dump.row({"item": "Coffee", "price": 4.50, "quantity": 2})
dump.row({"item": "Water", "price": None, "quantity": 3})
dump.close()
```

## DateTime Formatting

```python
dump = Dump(delimiter=" | ")

columns = [
    Column("event", "Event", str, 15),
    Column("timestamp", "Timestamp", datetime, 20),
    Column("status", "Status", str, 10),
]

dump.cols(columns)
dump.row({
    "event": "User Login",
    "timestamp": datetime(2024, 1, 15, 10, 30, 0),
    "status": "Success"
})
dump.close()
```

Output:
```
Event           | Timestamp            | Status    
--------------- | -------------------- | ----------
User Login      | 2024-01-15T10:30:00Z | Success   
Total rows: 1
```

## Header Separators

```python
# With separator (default)
dump = Dump()
columns = [Column("name", "Name", str, 10), Column("status", "Status", str, 8)]
dump.cols(columns)
dump.row({"name": "Alice", "status": "Active"})
dump.close()

# Without separator
dump = Dump(header_separator=False)
dump.cols(columns)
dump.row({"name": "Bob", "status": "Inactive"})
dump.close()
```

Output:
```
Name       Status  
---------- --------
Alice      Active  
Total rows: 1

Name       Status  
Bob        Inactive
Total rows: 1
```

## API Reference

### Column Class

```python
Column(
    name: str,
    display_name: str | None = None,
    type: type = str,
    width: int = 20,
    empty_value: str = "",
    truncate_suffix: str = "...",
    formatter: Callable[[Any], str] | None = None,
)
```

- `name`: Column name (used as dictionary key)
- `display_name`: Header display name (defaults to name)
- `type`: Data type (used for default formatting)
- `width`: Maximum column width
- `empty_value`: Value to display for None/empty values
- `truncate_suffix`: Suffix for truncated values
- `formatter`: Custom formatting function

### Dump Class

```python
Dump(
    delimiter: str = " ",
    ascii_box: bool = False,
    output_fn: Callable[[str], None] | None = None,
    header_separator: bool = True,
)
```

- `delimiter`: Separator between columns
- `ascii_box`: Enable ASCII box drawing
- `output_fn`: Custom output function (defaults to print)
- `header_separator`: Print separator line between header and data rows

#### Methods

- `cols(columns: Sequence[Column])`: Set columns and print header
- `row(data: dict[str, Any])`: Print a data row
- `close(summary: bool = True)`: Close table and optionally print summary

## License

MIT License
