#!/usr/bin/env python3
"""
Example demonstrating the RowDump library features.
"""

from datetime import datetime
from rowdump import Column, Dump


def main():
    """Demonstrate various RowDump features."""
    
    # Example 1: Basic usage
    print("=== Basic Usage ===")
    dump = Dump()
    
    columns = [
        Column("id", "ID", int, 5),
        Column("name", "Name", str, 15),
        Column("age", "Age", int, 3),
        Column("city", "City", str, 12),
    ]
    
    dump.cols(columns)
    
    # Add some rows
    dump.row({"id": 1, "name": "Alice", "age": 30, "city": "New York"})
    dump.row({"id": 2, "name": "Bob", "age": 25, "city": "San Francisco"})
    dump.row({"id": 3, "name": "Charlie", "age": 35, "city": "Los Angeles"})
    
    dump.close()
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: ASCII box formatting
    print("=== ASCII Box Formatting ===")
    dump_box = Dump(ascii_box=True)
    
    columns = [
        Column("product", "Product", str, 20),
        Column("price", "Price", float, 10),
        Column("stock", "Stock", int, 8),
    ]
    
    dump_box.cols(columns)
    
    dump_box.row({"product": "Laptop", "price": 999.99, "stock": 15})
    dump_box.row({"product": "Mouse", "price": 25.50, "stock": 100})
    dump_box.row({"product": "Keyboard", "price": 75.00, "stock": 50})
    
    dump_box.close()
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Custom delimiter and datetime formatting
    print("=== Custom Delimiter and DateTime ===")
    dump_custom = Dump(delimiter=" | ")
    
    columns = [
        Column("event", "Event", str, 15),
        Column("timestamp", "Timestamp", datetime, 20),
        Column("status", "Status", str, 10),
    ]
    
    dump_custom.cols(columns)
    
    dump_custom.row({
        "event": "User Login",
        "timestamp": datetime(2024, 1, 15, 10, 30, 0),
        "status": "Success"
    })
    dump_custom.row({
        "event": "File Upload",
        "timestamp": datetime(2024, 1, 15, 11, 45, 30),
        "status": "Failed"
    })
    
    dump_custom.close()
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Truncation and empty values
    print("=== Truncation and Empty Values ===")
    dump_trunc = Dump(ascii_box=True)
    
    columns = [
        Column("id", "ID", int, 3),
        Column("description", "Description", str, 15, empty_value="N/A"),
        Column("category", "Category", str, 8),
    ]
    
    dump_trunc.cols(columns)
    
    dump_trunc.row({
        "id": 1,
        "description": "This is a very long description that will be truncated",
        "category": "Electronics"
    })
    dump_trunc.row({
        "id": 2,
        "description": "",  # Empty value
        "category": "Books"
    })
    dump_trunc.row({
        "id": 3,
        "description": "Short desc",
        "category": "Clothing and Accessories"  # Will be truncated
    })
    
    dump_trunc.close()
    
    print("\n" + "="*50 + "\n")
    
    # Example 5: Custom formatter
    print("=== Custom Formatter ===")
    
    def currency_formatter(value):
        """Format numbers as currency."""
        if value is None:
            return "$0.00"
        return f"${value:.2f}"
    
    dump_fmt = Dump(ascii_box=True)
    
    columns = [
        Column("item", "Item", str, 12),
        Column("price", "Price", float, 10, formatter=currency_formatter),
        Column("quantity", "Qty", int, 5),
    ]
    
    dump_fmt.cols(columns)
    
    dump_fmt.row({"item": "Coffee", "price": 4.50, "quantity": 2})
    dump_fmt.row({"item": "Sandwich", "price": 12.99, "quantity": 1})
    dump_fmt.row({"item": "Water", "price": None, "quantity": 3})  # Will use formatter for None
    
    dump_fmt.close()
    
    print("\n" + "="*50 + "\n")
    
    # Example 6: Header separator options
    print("=== Header Separator Options ===")
    
    # With separator (default)
    print("With separator (default):")
    dump_sep = Dump()
    columns = [Column("name", "Name", str, 10), Column("status", "Status", str, 8)]
    dump_sep.cols(columns)
    dump_sep.row({"name": "Alice", "status": "Active"})
    dump_sep.row({"name": "Bob", "status": "Inactive"})
    dump_sep.close()
    
    print("\nWithout separator:")
    dump_no_sep = Dump(header_separator=False)
    dump_no_sep.cols(columns)
    dump_no_sep.row({"name": "Charlie", "status": "Active"})
    dump_no_sep.row({"name": "Diana", "status": "Pending"})
    dump_no_sep.close()
    
    print("\n" + "="*50 + "\n")
    
    # Example 7: Multiple tables
    print("=== Multiple Tables ===")
    dump_multi = Dump(ascii_box=True)
    
    # First table
    columns1 = [
        Column("name", "Name", str, 10),
        Column("score", "Score", int, 5),
    ]
    
    dump_multi.cols(columns1)
    dump_multi.row({"name": "Alice", "score": 95})
    dump_multi.row({"name": "Bob", "score": 87})
    dump_multi.close()
    
    # Second table - cols() automatically closes the previous table
    columns2 = [
        Column("product", "Product", str, 15),
        Column("revenue", "Revenue", float, 10),
    ]
    
    dump_multi.cols(columns2)
    dump_multi.row({"product": "Widget A", "revenue": 1500.00})
    dump_multi.row({"product": "Widget B", "revenue": 2300.50})
    dump_multi.close()


if __name__ == "__main__":
    main() 
