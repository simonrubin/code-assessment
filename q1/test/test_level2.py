"""
Level 2 Unit Tests

Comprehensive test suite for the Level 2 scan methods of the InMemoryDB class.
Run with: python -m pytest test/test_level2.py -v
"""

import pytest
import sys
import os

# Add parent directory to path to import impl
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from impl import InMemoryDB


class TestInMemoryDBLevel2:
    """Test cases for Level 2 methods of the InMemoryDB class."""
    
    def test_scan_empty_key(self):
        """Test scanning a key that doesn't exist."""
        db = InMemoryDB()
        
        # Scan non-existent key should return empty list
        assert db.scan("nonexistent") == []
    
    def test_scan_single_field(self):
        """Test scanning a key with a single field."""
        db = InMemoryDB()
        
        db.put("key1", "field1", "value1")
        result = db.scan("key1")
        assert result == ["field1(value1)"]
    
    def test_scan_multiple_fields_lexicographic_order(self):
        """Test scanning a key with multiple fields returns them in lexicographic order."""
        db = InMemoryDB()
        
        # Add fields in non-lexicographic order
        db.put("key1", "zebra", "z_value")
        db.put("key1", "apple", "a_value")
        db.put("key1", "banana", "b_value")
        
        result = db.scan("key1")
        expected = ["apple(a_value)", "banana(b_value)", "zebra(z_value)"]
        assert result == expected
    
    def test_scan_with_empty_values(self):
        """Test scanning with empty string values."""
        db = InMemoryDB()
        
        db.put("key1", "field1", "")
        db.put("key1", "field2", "not_empty")
        
        result = db.scan("key1")
        expected = ["field1()", "field2(not_empty)"]
        assert result == expected
    
    def test_scan_with_empty_fields(self):
        """Test scanning with empty string fields."""
        db = InMemoryDB()
        
        db.put("key1", "", "value1")
        db.put("key1", "field1", "value2")
        
        result = db.scan("key1")
        expected = ["(value1)", "field1(value2)"]
        assert result == expected
    
    def test_scan_with_special_characters(self):
        """Test scanning with special characters in fields and values."""
        db = InMemoryDB()
        
        db.put("key1", "field-with-dash", "value with spaces")
        db.put("key1", "field_with_underscore", "value@email.com")
        db.put("key1", "field.with.dots", "value/with/slashes")
        
        result = db.scan("key1")
        expected = [
            "field-with-dash(value with spaces)",
            "field.with.dots(value/with/slashes)",
            "field_with_underscore(value@email.com)"
        ]
        assert result == expected
    
    def test_scan_with_prefix_empty_key(self):
        """Test scan_with_prefix on a key that doesn't exist."""
        db = InMemoryDB()
        
        assert db.scan_with_prefix("nonexistent", "prefix") == []
    
    def test_scan_with_prefix_no_matches(self):
        """Test scan_with_prefix when no fields match the prefix."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "banana", "value2")
        
        result = db.scan_with_prefix("key1", "z")
        assert result == []
    
    def test_scan_with_prefix_single_match(self):
        """Test scan_with_prefix with a single matching field."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "banana", "value2")
        db.put("key1", "zebra", "value3")
        
        result = db.scan_with_prefix("key1", "a")
        assert result == ["apple(value1)"]
    
    def test_scan_with_prefix_multiple_matches(self):
        """Test scan_with_prefix with multiple matching fields."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "apricot", "value2")
        db.put("key1", "banana", "value3")
        db.put("key1", "avocado", "value4")
        
        result = db.scan_with_prefix("key1", "a")
        expected = ["apple(value1)", "apricot(value2)", "avocado(value4)"]
        assert result == expected
    
    def test_scan_with_prefix_exact_match(self):
        """Test scan_with_prefix with exact field name match."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "apples", "value2")
        
        result = db.scan_with_prefix("key1", "apple")
        assert result == ["apple(value1)", "apples(value2)"]
    
    def test_scan_with_prefix_empty_prefix(self):
        """Test scan_with_prefix with empty prefix (should return all fields)."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "banana", "value2")
        
        result = db.scan_with_prefix("key1", "")
        expected = ["apple(value1)", "banana(value2)"]
        assert result == expected
    
    def test_scan_with_prefix_case_sensitive(self):
        """Test that scan_with_prefix is case sensitive."""
        db = InMemoryDB()
        
        db.put("key1", "Apple", "value1")
        db.put("key1", "apple", "value2")
        db.put("key1", "APPLE", "value3")
        
        result = db.scan_with_prefix("key1", "a")
        assert result == ["apple(value2)"]
        
        result = db.scan_with_prefix("key1", "A")
        expected = ["APPLE(value3)", "Apple(value1)"]
        assert result == expected
    
    def test_scan_with_prefix_after_deletion(self):
        """Test scan_with_prefix after deleting fields."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "apricot", "value2")
        db.put("key1", "banana", "value3")
        
        # Delete one field
        db.delete("key1", "apricot")
        
        result = db.scan_with_prefix("key1", "a")
        assert result == ["apple(value1)"]
        
        result = db.scan("key1")
        expected = ["apple(value1)", "banana(value3)"]
        assert result == expected
    
    def test_scan_with_prefix_after_overwrite(self):
        """Test scan_with_prefix after overwriting field values."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "old_value")
        db.put("key1", "apricot", "value2")
        
        # Overwrite apple's value
        db.put("key1", "apple", "new_value")
        
        result = db.scan_with_prefix("key1", "a")
        expected = ["apple(new_value)", "apricot(value2)"]
        assert result == expected
    
    def test_scan_with_prefix_multiple_keys(self):
        """Test scan_with_prefix doesn't affect other keys."""
        db = InMemoryDB()
        
        db.put("key1", "apple", "value1")
        db.put("key1", "apricot", "value2")
        db.put("key2", "apple", "value3")
        db.put("key2", "banana", "value4")
        
        result = db.scan_with_prefix("key1", "a")
        expected = ["apple(value1)", "apricot(value2)"]
        assert result == expected
        
        result = db.scan_with_prefix("key2", "a")
        assert result == ["apple(value3)"]
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple operations."""
        db = InMemoryDB()
        
        # Setup multiple users with various fields
        db.put("user1", "name", "Alice")
        db.put("user1", "email", "alice@example.com")
        db.put("user1", "age", "25")
        db.put("user1", "address", "123 Main St")
        
        db.put("user2", "name", "Bob")
        db.put("user2", "email", "bob@example.com")
        db.put("user2", "phone", "555-1234")
        
        # Test scan on user1
        result = db.scan("user1")
        expected = ["address(123 Main St)", "age(25)", "email(alice@example.com)", "name(Alice)"]
        assert result == expected
        
        # Test scan_with_prefix on user1
        result = db.scan_with_prefix("user1", "a")
        expected = ["address(123 Main St)", "age(25)"]
        assert result == expected
        
        # Test scan_with_prefix on user2
        result = db.scan_with_prefix("user2", "e")
        assert result == ["email(bob@example.com)"]
        
        # Delete a field and test again
        db.delete("user1", "age")
        result = db.scan("user1")
        expected = ["address(123 Main St)", "email(alice@example.com)", "name(Alice)"]
        assert result == expected
        
        result = db.scan_with_prefix("user1", "a")
        assert result == ["address(123 Main St)"]
    
    def test_scan_with_prefix_edge_cases(self):
        """Test edge cases for scan_with_prefix."""
        db = InMemoryDB()
        
        # Test with fields that are substrings of each other
        db.put("key1", "a", "value1")
        db.put("key1", "ab", "value2")
        db.put("key1", "abc", "value3")
        
        result = db.scan_with_prefix("key1", "a")
        expected = ["a(value1)", "ab(value2)", "abc(value3)"]
        assert result == expected
        
        result = db.scan_with_prefix("key1", "ab")
        expected = ["ab(value2)", "abc(value3)"]
        assert result == expected
        
        result = db.scan_with_prefix("key1", "abc")
        assert result == ["abc(value3)"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
