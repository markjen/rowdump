"""
Tests for the RowDump library.
"""

import io
from datetime import datetime
from rowdump import Column, Dump


class TestColumn:
    """Test Column class functionality."""
    
    def test_column_init(self):
        """Test Column initialization."""
        col = Column("test", "Test Column", str, 10)
        assert col.name == "test"
        assert col.display_name == "Test Column"
        assert col.type == str
        assert col.width == 10
        assert col.empty_value == ""
        assert col.truncate_suffix == "..."
        
    def test_column_defaults(self):
        """Test Column with default values."""
        col = Column("test")
        assert col.name == "test"
        assert col.display_name == "test"  # Should use name as display_name
        assert col.type == str
        assert col.width == 20
        
    def test_format_value_basic(self):
        """Test basic value formatting."""
        col = Column("test", width=10)
        
        # Normal value
        assert col.format_value("hello") == "hello"
        
        # None value
        assert col.format_value(None) == ""
        
        # Empty string
        assert col.format_value("") == ""
        
    def test_format_value_truncation(self):
        """Test value truncation."""
        col = Column("test", width=10)
        
        # Value that needs truncation
        long_value = "this is a very long string"
        formatted = col.format_value(long_value)
        assert len(formatted) == 10
        assert formatted.endswith("...")
        assert formatted == "this is..."
        
    def test_format_value_empty_value(self):
        """Test custom empty value."""
        col = Column("test", width=10, empty_value="N/A")
        
        assert col.format_value(None) == "N/A"
        assert col.format_value("") == "N/A"
        
    def test_format_value_datetime(self):
        """Test datetime formatting."""
        col = Column("test", type=datetime, width=20)
        
        # UTC datetime (no timezone)
        dt = datetime(2024, 1, 15, 10, 30, 0)
        formatted = col.format_value(dt)
        assert formatted == "2024-01-15T10:30:00Z"
        
    def test_custom_formatter(self):
        """Test custom formatter function."""
        def custom_fmt(value):
            return f"Custom: {value}"
            
        col = Column("test", width=20, formatter=custom_fmt)
        
        formatted = col.format_value("hello")
        assert formatted == "Custom: hello"


class TestDump:
    """Test Dump class functionality."""
    
    def test_dump_init(self):
        """Test Dump initialization."""
        dump = Dump()
        assert dump.delimiter == " "
        assert dump.ascii_box is False
        assert dump.output_fn is not None
        
    def test_dump_custom_params(self):
        """Test Dump with custom parameters."""
        output_buffer = io.StringIO()
        
        def custom_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(delimiter=" | ", ascii_box=True, output_fn=custom_output)
        assert dump.delimiter == " | "
        assert dump.ascii_box is True
        assert dump.output_fn == custom_output
        
    def test_simple_table(self):
        """Test basic table output."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(output_fn=capture_output)
        
        columns = [
            Column("id", "ID", int, 5),
            Column("name", "Name", str, 10),
        ]
        
        dump.cols(columns)
        dump.row({"id": 1, "name": "Alice"})
        dump.row({"id": 2, "name": "Bob"})
        dump.close()
        
        output = output_buffer.getvalue()
        lines = output.strip().split('\n')
        
        # Check header
        assert "ID" in lines[0]
        assert "Name" in lines[0]
        
        # Check separator line (new default behavior)
        assert "-----" in lines[1]
        
        # Check data rows (now at lines 2 and 3)
        assert "1" in lines[2]
        assert "Alice" in lines[2]
        assert "2" in lines[3]
        assert "Bob" in lines[3]
        
        # Check summary
        assert "Total rows: 2" in lines[4]
        
    def test_ascii_box_table(self):
        """Test ASCII box table output."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(ascii_box=True, output_fn=capture_output)
        
        columns = [
            Column("id", "ID", int, 3),
            Column("name", "Name", str, 5),
        ]
        
        dump.cols(columns)
        dump.row({"id": 1, "name": "Alice"})
        dump.close()
        
        output = output_buffer.getvalue()
        lines = output.strip().split('\n')
        
        # Check box characters are present
        assert "┌" in lines[0]  # Top border
        assert "│" in lines[1]  # Header row
        assert "├" in lines[2]  # Separator
        assert "│" in lines[3]  # Data row
        assert "└" in lines[4]  # Bottom border
        
    def test_custom_delimiter(self):
        """Test custom delimiter."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(delimiter=" | ", output_fn=capture_output)
        
        columns = [
            Column("a", "A", str, 5),
            Column("b", "B", str, 5),
        ]
        
        dump.cols(columns)
        dump.row({"a": "test1", "b": "test2"})
        dump.close()
        
        output = output_buffer.getvalue()
        lines = output.strip().split('\n')
        
        # Check delimiter in header
        assert " | " in lines[0]
        
        # Check delimiter in separator line
        assert " | " in lines[1]
        
        # Check delimiter in data row
        assert " | " in lines[2]
        
    def test_multiple_tables(self):
        """Test multiple tables with the same Dump instance."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(ascii_box=True, output_fn=capture_output)
        
        # First table
        columns1 = [Column("a", "A", str, 5)]
        dump.cols(columns1)
        dump.row({"a": "test1"})
        dump.close()
        
        # Second table
        columns2 = [Column("b", "B", str, 5)]
        dump.cols(columns2)
        dump.row({"b": "test2"})
        dump.close()
        
        output = output_buffer.getvalue()
        lines = output.strip().split('\n')
        
        # Should have two separate tables with summaries
        assert "Total rows: 1" in output
        assert output.count("Total rows: 1") == 2
        
    def test_no_summary(self):
        """Test closing without summary."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(output_fn=capture_output)
        
        columns = [Column("test", "Test", str, 5)]
        dump.cols(columns)
        dump.row({"test": "value"})
        dump.close(summary=False)
        
        output = output_buffer.getvalue()
        assert "Total rows:" not in output
        
    def test_extra_keys_ignored(self):
        """Test that extra keys in row data are ignored."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        dump = Dump(output_fn=capture_output)
        
        columns = [Column("name", "Name", str, 10)]
        dump.cols(columns)
        dump.row({"name": "Alice", "extra_key": "ignored"})
        dump.close()
        
        output = output_buffer.getvalue()
        # Should not contain the extra key
        assert "ignored" not in output
        assert "Alice" in output
        
    def test_header_separator_flag(self):
        """Test header_separator flag functionality."""
        output_buffer = io.StringIO()
        
        def capture_output(text):
            output_buffer.write(text + "\n")
            
        # Test with header_separator=True (default)
        dump = Dump(output_fn=capture_output, header_separator=True)
        columns = [Column("name", "Name", str, 10)]
        dump.cols(columns)
        dump.row({"name": "Alice"})
        dump.close()
        
        output_with_separator = output_buffer.getvalue()
        lines_with_separator = output_with_separator.strip().split('\n')
        
        # Should have separator line
        assert "-----" in lines_with_separator[1]
        
        # Test with header_separator=False
        output_buffer = io.StringIO()
        dump = Dump(output_fn=capture_output, header_separator=False)
        dump.cols(columns)
        dump.row({"name": "Bob"})
        dump.close()
        
        output_without_separator = output_buffer.getvalue()
        lines_without_separator = output_without_separator.strip().split('\n')
        
        # Should not have separator line - data row should be at line 1
        assert "Bob" in lines_without_separator[1]
        assert "-----" not in output_without_separator


def test_datetime_formatting():
    """Test datetime formatting in different scenarios."""
    col = Column("dt", type=datetime, width=25)
    
    # Test naive datetime (no timezone)
    dt_naive = datetime(2024, 1, 15, 10, 30, 0)
    formatted = col.format_value(dt_naive)
    assert formatted == "2024-01-15T10:30:00Z"
    
    # Test with timezone info would require more complex setup
    # For now, just test the basic case


def test_integration_example():
    """Integration test simulating the example usage."""
    output_buffer = io.StringIO()
    
    def capture_output(text):
        output_buffer.write(text + "\n")
        
    dump = Dump(ascii_box=True, output_fn=capture_output)
    
    columns = [
        Column("id", "ID", int, 5),
        Column("name", "Name", str, 15),
        Column("description", "Description", str, 20, empty_value="N/A"),
    ]
    
    dump.cols(columns)
    
    # Test various scenarios
    dump.row({"id": 1, "name": "Alice", "description": "Software Engineer"})
    dump.row({"id": 2, "name": "Bob", "description": ""})  # Empty description
    dump.row({"id": 3, "name": "Charlie", "description": "This is a very long description that will be truncated"})
    
    dump.close()
    
    output = output_buffer.getvalue()
    
    # Verify key elements are present
    assert "Alice" in output
    assert "Bob" in output
    assert "Charlie" in output
    assert "N/A" in output  # Empty value replacement
    assert "..." in output  # Truncation
    assert "Total rows: 3" in output 
