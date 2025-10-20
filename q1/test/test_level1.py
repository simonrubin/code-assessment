"""
Level 1 Unit Tests

Comprehensive test suite for the InMemoryDB class.
Run with: python -m pytest test/test_level1.py -v
"""

import pytest
import sys
import os

# Add parent directory to path to import impl
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from impl import InMemoryDB


class TestInMemoryDB:
    """Test cases for the InMemoryDB class."""
    
    def test_empty_database(self):
        """Test operations on an empty database."""
        db = InMemoryDB()
        
        # Getting from empty database should return None
        assert db.get("nonexistent", "field") is None
        
        # Deleting from empty database should return False
        assert db.delete("nonexistent", "field") is False
    
    def test_basic_put_and_get(self):
        """Test basic put and get operations."""
        db = InMemoryDB()
        
        # Put a value and retrieve it
        db.put("key1", "field1", "value1")
        assert db.get("key1", "field1") == "value1"
        
        # Put another value for the same key
        db.put("key1", "field2", "value2")
        assert db.get("key1", "field2") == "value2"
        
        # Verify first value is still there
        assert db.get("key1", "field1") == "value1"
    
    def test_multiple_keys(self):
        """Test operations with multiple keys."""
        db = InMemoryDB()
        
        # Put values for different keys
        db.put("key1", "field1", "value1")
        db.put("key2", "field1", "value2")
        db.put("key2", "field2", "value3")
        
        # Verify values are stored correctly
        assert db.get("key1", "field1") == "value1"
        assert db.get("key2", "field1") == "value2"
        assert db.get("key2", "field2") == "value3"
        
        # Verify cross-key contamination doesn't occur
        assert db.get("key1", "field2") is None
        assert db.get("key2", "field1") == "value2"  # Should not be affected by key1
    
    def test_overwrite_values(self):
        """Test that putting a value overwrites existing values."""
        db = InMemoryDB()
        
        # Put initial value
        db.put("key1", "field1", "original")
        assert db.get("key1", "field1") == "original"
        
        # Overwrite with new value
        db.put("key1", "field1", "updated")
        assert db.get("key1", "field1") == "updated"
    
    def test_delete_existing_field(self):
        """Test deleting an existing field."""
        db = InMemoryDB()
        
        # Put a value
        db.put("key1", "field1", "value1")
        assert db.get("key1", "field1") == "value1"
        
        # Delete the field
        assert db.delete("key1", "field1") is True
        
        # Verify field is gone
        assert db.get("key1", "field1") is None
    
    def test_delete_nonexistent_field(self):
        """Test deleting a field that doesn't exist."""
        db = InMemoryDB()
        
        # Try to delete non-existent field
        assert db.delete("key1", "nonexistent") is False
        
        # Put a value for a different field
        db.put("key1", "field1", "value1")
        
        # Try to delete different non-existent field
        assert db.delete("key1", "nonexistent") is False
        
        # Original field should still exist
        assert db.get("key1", "field1") == "value1"
    
    def test_delete_nonexistent_key(self):
        """Test deleting from a key that doesn't exist."""
        db = InMemoryDB()
        
        # Try to delete from non-existent key
        assert db.delete("nonexistent", "field1") is False
    
    def test_delete_partial_key(self):
        """Test that deleting one field doesn't affect other fields."""
        db = InMemoryDB()
        
        # Put multiple fields for same key
        db.put("key1", "field1", "value1")
        db.put("key1", "field2", "value2")
        db.put("key1", "field3", "value3")
        
        # Delete one field
        assert db.delete("key1", "field2") is True
        
        # Verify other fields are still there
        assert db.get("key1", "field1") == "value1"
        assert db.get("key1", "field3") == "value3"
        
        # Verify deleted field is gone
        assert db.get("key1", "field2") is None
    
    def test_empty_string_values(self):
        """Test handling of empty string values."""
        db = InMemoryDB()
        
        # Put empty string value
        db.put("key1", "field1", "")
        assert db.get("key1", "field1") == ""
        
        # Put non-empty value
        db.put("key1", "field2", "not_empty")
        assert db.get("key1", "field2") == "not_empty"
    
    def test_empty_string_keys_and_fields(self):
        """Test handling of empty string keys and fields."""
        db = InMemoryDB()
        
        # Put with empty key
        db.put("", "field1", "value1")
        assert db.get("", "field1") == "value1"
        
        # Put with empty field
        db.put("key1", "", "value2")
        assert db.get("key1", "") == "value2"
        
        # Put with both empty
        db.put("", "", "value3")
        assert db.get("", "") == "value3"
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple operations."""
        db = InMemoryDB()
        
        # Initial setup
        db.put("user1", "name", "Alice")
        db.put("user1", "email", "alice@example.com")
        db.put("user2", "name", "Bob")
        db.put("user2", "email", "bob@example.com")
        
        # Verify initial state
        assert db.get("user1", "name") == "Alice"
        assert db.get("user1", "email") == "alice@example.com"
        assert db.get("user2", "name") == "Bob"
        assert db.get("user2", "email") == "bob@example.com"
        
        # Update Alice's email
        db.put("user1", "email", "alice.new@example.com")
        assert db.get("user1", "email") == "alice.new@example.com"
        assert db.get("user1", "name") == "Alice"  # Should be unchanged
        
        # Delete Bob's email
        assert db.delete("user2", "email") is True
        assert db.get("user2", "email") is None
        assert db.get("user2", "name") == "Bob"  # Should be unchanged
        
        # Try to delete Bob's email again
        assert db.delete("user2", "email") is False
        
        # Add new field for Alice
        db.put("user1", "age", "25")
        assert db.get("user1", "age") == "25"
        
        # Verify all other fields still exist
        assert db.get("user1", "name") == "Alice"
        assert db.get("user1", "email") == "alice.new@example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
