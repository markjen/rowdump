"""
Core classes for RowDump library.
"""

from collections.abc import Callable, Sequence
from datetime import datetime
from typing import Any


class Column:
    """
    Represents a column definition for table output.

    Attributes:
        name: The column name (used as key in row data)
        display_name: The name shown in the header
        type: The expected data type (used for default formatting)
        width: The maximum width for the column
        empty_value: What to display when the value is None or empty
        truncate_suffix: What to append when truncating (default: "...")
        formatter: Custom formatting function
    """

    def __init__(
        self,
        name: str,
        display_name: str | None = None,
        type: type = str,
        width: int = 20,
        empty_value: str = "",
        truncate_suffix: str = "...",
        formatter: Callable[[Any], str] | None = None,
    ):
        self.name = name
        self.display_name = display_name or name
        self.type = type
        self.width = width
        self.empty_value = empty_value
        self.truncate_suffix = truncate_suffix
        self.formatter = formatter or self._default_formatter

    def _default_formatter(self, value: Any) -> str:
        """Default formatter based on column type."""
        if value is None:
            return self.empty_value

        if self.type == datetime and isinstance(value, datetime):
            # RFC3339 format, no millis, Z for UTC
            if value.tzinfo is None:
                return value.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                return value.strftime("%Y-%m-%dT%H:%M:%S%z")

        return str(value)

    def format_value(self, value: Any) -> str:
        """Format and truncate value according to column settings."""
        # For default formatter, check empty values first
        if self.formatter == self._default_formatter:
            if value is None or (isinstance(value, str) and not value):
                formatted = self.empty_value
            else:
                formatted = self.formatter(value)
        else:
            # Custom formatter handles all values, including None
            formatted = self.formatter(value)

        # Truncate if necessary
        if len(formatted) > self.width:
            if len(self.truncate_suffix) >= self.width:
                return self.truncate_suffix[:self.width]
            return formatted[:self.width - len(self.truncate_suffix)] + self.truncate_suffix

        return formatted


class Dump:
    """
    Main class for creating formatted table output.

    Supports customizable column definitions, delimiters, ASCII box drawing,
    header separators, and custom output functions.
    """

    def __init__(
        self,
        delimiter: str = " ",
        ascii_box: bool = False,
        output_fn: Callable[[str], None] | None = None,
        header_separator: bool = True,
    ):
        self.delimiter = delimiter
        self.ascii_box = ascii_box
        self.output_fn = output_fn or print
        self.header_separator = header_separator
        self._columns: list[Column] = []
        self._row_count = 0
        self._table_active = False

    def cols(self, columns: Sequence[Column]) -> None:
        """
        Set column definitions and print header row.

        Args:
            columns: Sequence of Column objects defining the table structure
        """
        # Close previous table if active
        if self._table_active:
            self._close_table()
            self.output_fn("")  # Line break between tables

        self._columns = list(columns)
        self._row_count = 0
        self._table_active = True

        # Print header
        self._print_header()

    def _print_header(self) -> None:
        """Print the table header."""
        if not self._columns:
            return

        if self.ascii_box:
            self._print_box_top()
            self._print_box_header()
            if self.header_separator:
                self._print_box_separator()
        else:
            self._print_simple_header()
            if self.header_separator:
                self._print_simple_separator()

    def _print_box_top(self) -> None:
        """Print the top border of ASCII box."""
        parts = []
        for col in self._columns:
            parts.append("─" * col.width)
        line = "┌" + "┬".join(parts) + "┐"
        self.output_fn(line)

    def _print_box_header(self) -> None:
        """Print header row with box formatting."""
        parts = []
        for col in self._columns:
            display_text = col.display_name
            if len(display_text) > col.width:
                if len(col.truncate_suffix) >= col.width:
                    display_text = col.truncate_suffix[:col.width]
                else:
                    display_text = display_text[:col.width - len(col.truncate_suffix)] + col.truncate_suffix
            parts.append(display_text.ljust(col.width))
        line = "│" + "│".join(parts) + "│"
        self.output_fn(line)

    def _print_box_separator(self) -> None:
        """Print separator line in box format."""
        parts = []
        for col in self._columns:
            parts.append("─" * col.width)
        line = "├" + "┼".join(parts) + "┤"
        self.output_fn(line)

    def _print_simple_header(self) -> None:
        """Print simple header without box."""
        parts = []
        for col in self._columns:
            display_text = col.display_name
            if len(display_text) > col.width:
                if len(col.truncate_suffix) >= col.width:
                    display_text = col.truncate_suffix[:col.width]
                else:
                    display_text = display_text[:col.width - len(col.truncate_suffix)] + col.truncate_suffix
            parts.append(display_text.ljust(col.width))
        self.output_fn(self.delimiter.join(parts))

    def _print_simple_separator(self) -> None:
        """Print separator line for simple header."""
        parts = []
        for col in self._columns:
            parts.append("-" * col.width)
        self.output_fn(self.delimiter.join(parts))

    def row(self, data: dict[str, Any]) -> None:
        """
        Print a data row.

        Args:
            data: Dictionary mapping column names to values
        """
        if not self._columns:
            return

        self._row_count += 1

        if self.ascii_box:
            self._print_box_row(data)
        else:
            self._print_simple_row(data)

    def _print_box_row(self, data: dict[str, Any]) -> None:
        """Print data row with box formatting."""
        parts = []
        for col in self._columns:
            value = data.get(col.name)
            formatted_value = col.format_value(value)
            parts.append(formatted_value.ljust(col.width))
        line = "│" + "│".join(parts) + "│"
        self.output_fn(line)

    def _print_simple_row(self, data: dict[str, Any]) -> None:
        """Print simple data row without box."""
        parts = []
        for col in self._columns:
            value = data.get(col.name)
            formatted_value = col.format_value(value)
            parts.append(formatted_value.ljust(col.width))
        self.output_fn(self.delimiter.join(parts))

    def _close_table(self) -> None:
        """Close the current table if using ASCII box."""
        if self.ascii_box and self._table_active:
            self._print_box_bottom()

    def _print_box_bottom(self) -> None:
        """Print the bottom border of ASCII box."""
        parts = []
        for col in self._columns:
            parts.append("─" * col.width)
        line = "└" + "┴".join(parts) + "┘"
        self.output_fn(line)

    def close(self, summary: bool = True) -> None:
        """
        Close the table and optionally print summary.

        Args:
            summary: Whether to print row count summary
        """
        if self._table_active:
            self._close_table()

            if summary:
                self.output_fn(f"Total rows: {self._row_count}")

            self._table_active = False
