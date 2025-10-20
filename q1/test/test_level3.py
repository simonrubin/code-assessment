"""
Level 3 Unit Tests

Comprehensive test suite for the Level 3 timestamp-based methods with TTL support.
Run with: python -m pytest test/test_level3.py -v
"""

import pytest
import sys
import os

# Add parent directory to path to import impl
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from impl import InMemoryDB


class TestInMemoryDBLevel3:
    """Test cases for Level 3 timestamp-based methods of the InMemoryDB class."""
    
    def test_put_at_and_get_at_basic(self):
        """Test basic put_at and get_at operations."""
        db = InMemoryDB()
        
        # Put at timestamp 100
        db.put_at(100, "key1", "field1", "value1")
        
        # Get at same timestamp should work
        assert db.get_at(100, "key1", "field1") == "value1"
        
        # Get at earlier timestamp should return None
        assert db.get_at(50, "key1", "field1") is None
        
        # Get at later timestamp should still work (no TTL)
        assert db.get_at(200, "key1", "field1") == "value1"
    
    def test_put_at_with_ttl_basic(self):
        """Test basic TTL functionality."""
        db = InMemoryDB()
        
        # Put with TTL at timestamp 100, expires at 150
        db.put_at_with_ttl(100, "key1", "field1", "value1", 50)
        
        # Should be available before expiration
        assert db.get_at(120, "key1", "field1") == "value1"
        assert db.get_at(149, "key1", "field1") == "value1"
        
        # Should be None at and after expiration
        assert db.get_at(150, "key1", "field1") is None
        assert db.get_at(200, "key1", "field1") is None
    
    def test_delete_at_basic(self):
        """Test basic delete_at operation."""
        db = InMemoryDB()
        
        # Put at timestamp 100
        db.put_at(100, "key1", "field1", "value1")
        
        # Delete at timestamp 150 should work
        assert db.delete_at(150, "key1", "field1") is True
        
        # Should be gone after deletion
        assert db.get_at(200, "key1", "field1") is None
        
        # Try to delete again should return False
        assert db.delete_at(200, "key1", "field1") is False
    
    def test_delete_at_expired_entry(self):
        """Test delete_at on expired entries."""
        db = InMemoryDB()
        
        # Put with TTL at timestamp 100, expires at 150
        db.put_at_with_ttl(100, "key1", "field1", "value1", 50)
        
        # Try to delete before expiration should work
        assert db.delete_at(120, "key1", "field1") is True
        
        # Put again with TTL
        db.put_at_with_ttl(100, "key1", "field1", "value1", 50)
        
        # Try to delete after expiration should return False
        assert db.delete_at(160, "key1", "field1") is False
    
    def test_scan_at_basic(self):
        """Test basic scan_at operation."""
        db = InMemoryDB()
        
        # Put multiple fields at different timestamps
        db.put_at(100, "key1", "apple", "value1")
        db.put_at(120, "key1", "banana", "value2")
        db.put_at(110, "key1", "cherry", "value3")
        
        # Scan at timestamp 130 should return all fields in lexicographic order
        result = db.scan_at(130, "key1")
        expected = ["apple(value1)", "banana(value2)", "cherry(value3)"]
        assert result == expected
    
    def test_scan_at_with_expired_entries(self):
        """Test scan_at ignores expired entries."""
        db = InMemoryDB()
        
        # Put permanent entry
        db.put_at(100, "key1", "permanent", "value1")
        
        # Put TTL entry that expires at 150
        db.put_at_with_ttl(100, "key1", "temporary", "value2", 50)
        
        # Scan before expiration should include both
        result = db.scan_at(120, "key1")
        expected = ["permanent(value1)", "temporary(value2)"]
        assert result == expected
        
        # Scan after expiration should only include permanent
        result = db.scan_at(160, "key1")
        expected = ["permanent(value1)"]
        assert result == expected
    
    def test_scan_with_prefix_at_basic(self):
        """Test basic scan_with_prefix_at operation."""
        db = InMemoryDB()
        
        # Put fields with different prefixes
        db.put_at(100, "key1", "apple", "value1")
        db.put_at(100, "key1", "apricot", "value2")
        db.put_at(100, "key1", "banana", "value3")
        
        # Scan with prefix "a" should return apple and apricot
        result = db.scan_with_prefix_at(120, "key1", "a")
        expected = ["apple(value1)", "apricot(value2)"]
        assert result == expected
    
    def test_scan_with_prefix_at_with_expired_entries(self):
        """Test scan_with_prefix_at ignores expired entries."""
        db = InMemoryDB()
        
        # Put permanent entries
        db.put_at(100, "key1", "apple", "value1")
        db.put_at(100, "key1", "apricot", "value2")
        
        # Put TTL entry that expires at 150
        db.put_at_with_ttl(100, "key1", "avocado", "value3", 50)
        
        # Scan with prefix "a" before expiration should include all
        result = db.scan_with_prefix_at(120, "key1", "a")
        expected = ["apple(value1)", "apricot(value2)", "avocado(value3)"]
        assert result == expected
        
        # Scan with prefix "a" after expiration should exclude avocado
        result = db.scan_with_prefix_at(160, "key1", "a")
        expected = ["apple(value1)", "apricot(value2)"]
        assert result == expected
    
    def test_multiple_timestamps_same_key_field(self):
        """Test multiple operations at different timestamps on same key-field."""
        db = InMemoryDB()
        
        # Put at timestamp 100
        db.put_at(100, "key1", "field1", "value1")
        assert db.get_at(100, "key1", "field1") == "value1"
        
        # Overwrite at timestamp 150
        db.put_at(150, "key1", "field1", "value2")
        assert db.get_at(100, "key1", "field1") == "value1"  # Still old value
        assert db.get_at(150, "key1", "field1") == "value2"  # New value
        assert db.get_at(200, "key1", "field1") == "value2"  # Latest value
        
        # Put with TTL at timestamp 200, expires at 250
        db.put_at_with_ttl(200, "key1", "field1", "value3", 50)
        assert db.get_at(200, "key1", "field1") == "value3"
        assert db.get_at(240, "key1", "field1") == "value3"
        assert db.get_at(250, "key1", "field1") is None  # Expired
    
    def test_ttl_overwrites_permanent_entry(self):
        """Test that TTL entries can overwrite permanent entries."""
        db = InMemoryDB()
        
        # Put permanent entry
        db.put_at(100, "key1", "field1", "permanent")
        assert db.get_at(200, "key1", "field1") == "permanent"
        
        # Overwrite with TTL entry
        db.put_at_with_ttl(150, "key1", "field1", "temporary", 50)
        assert db.get_at(150, "key1", "field1") == "temporary"
        assert db.get_at(199, "key1", "field1") == "temporary"
        assert db.get_at(200, "key1", "field1") is None  # Expired
        assert db.get_at(250, "key1", "field1") is None  # Still expired
    
    def test_permanent_entry_overwrites_ttl(self):
        """Test that permanent entries can overwrite TTL entries."""
        db = InMemoryDB()
        
        # Put TTL entry
        db.put_at_with_ttl(100, "key1", "field1", "temporary", 50)
        assert db.get_at(120, "key1", "field1") == "temporary"
        assert db.get_at(150, "key1", "field1") is None  # Expired
        
        # Overwrite with permanent entry before expiration
        db.put_at(130, "key1", "field1", "permanent")
        assert db.get_at(130, "key1", "field1") == "permanent"
        assert db.get_at(200, "key1", "field1") == "permanent"  # Still there
    
    def test_scan_at_empty_key(self):
        """Test scan_at on empty or non-existent key."""
        db = InMemoryDB()
        
        # Scan non-existent key should return empty list
        assert db.scan_at(100, "nonexistent") == []
        
        # Put and then scan before timestamp should return empty
        db.put_at(100, "key1", "field1", "value1")
        assert db.scan_at(50, "key1") == []
    
    def test_scan_with_prefix_at_empty_key(self):
        """Test scan_with_prefix_at on empty or non-existent key."""
        db = InMemoryDB()
        
        # Scan non-existent key should return empty list
        assert db.scan_with_prefix_at(100, "nonexistent", "prefix") == []
        
        # Put and then scan before timestamp should return empty
        db.put_at(100, "key1", "field1", "value1")
        assert db.scan_with_prefix_at(50, "key1", "f") == []
    
    def test_ttl_zero_and_negative(self):
        """Test edge cases with TTL values."""
        db = InMemoryDB()
        
        # TTL of 0 should expire immediately
        db.put_at_with_ttl(100, "key1", "field1", "value1", 0)
        assert db.get_at(100, "key1", "field1") is None
        
        # TTL of 1 should expire at next timestamp
        db.put_at_with_ttl(100, "key1", "field2", "value2", 1)
        assert db.get_at(100, "key1", "field2") == "value2"
        assert db.get_at(101, "key1", "field2") is None
    
    def test_multiple_keys_timestamp_operations(self):
        """Test timestamp operations don't interfere between keys."""
        db = InMemoryDB()
        
        # Put different values for different keys at same timestamp
        db.put_at(100, "key1", "field1", "value1")
        db.put_at(100, "key2", "field1", "value2")
        
        # Put with TTL for key1
        db.put_at_with_ttl(100, "key1", "field1", "ttl_value", 50)
        
        # Key2 should be unaffected
        assert db.get_at(200, "key2", "field1") == "value2"
        
        # Key1 should be expired
        assert db.get_at(200, "key1", "field1") is None
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple operations and TTL."""
        db = InMemoryDB()
        
        # Setup: User session management
        db.put_at(100, "user1", "name", "Alice")  # Permanent
        db.put_at_with_ttl(100, "user1", "session", "abc123", 100)  # Expires at 200
        db.put_at_with_ttl(100, "user1", "temp_data", "temp", 50)  # Expires at 150
        
        # At timestamp 120 - all should be available
        result = db.scan_at(120, "user1")
        expected = ["name(Alice)", "session(abc123)", "temp_data(temp)"]
        assert result == expected
        
        # At timestamp 160 - temp_data should be expired
        result = db.scan_at(160, "user1")
        expected = ["name(Alice)", "session(abc123)"]
        assert result == expected
        
        # At timestamp 220 - only name should remain
        result = db.scan_at(220, "user1")
        expected = ["name(Alice)"]
        assert result == expected
        
        # Test prefix scan at different timestamps
        result = db.scan_with_prefix_at(120, "user1", "s")
        assert result == ["session(abc123)"]
        
        result = db.scan_with_prefix_at(160, "user1", "s")
        assert result == ["session(abc123)"]
        
        result = db.scan_with_prefix_at(220, "user1", "s")
        assert result == []
        
        # Test deletion of expired entry
        assert db.delete_at(220, "user1", "session") is False
        
        # Test deletion of permanent entry
        assert db.delete_at(220, "user1", "name") is True
        assert db.scan_at(220, "user1") == []
    
    def test_ttl_precision(self):
        """Test TTL expiration timing precision."""
        db = InMemoryDB()
        
        # Put with TTL at timestamp 100, expires at 150
        db.put_at_with_ttl(100, "key1", "field1", "value1", 50)
        
        # Test exact expiration boundary
        assert db.get_at(149, "key1", "field1") == "value1"  # Not expired
        assert db.get_at(150, "key1", "field1") is None     # Expired
        assert db.get_at(151, "key1", "field1") is None     # Still expired
    
    def test_scan_at_lexicographic_order_with_timestamps(self):
        """Test that scan_at maintains lexicographic order regardless of timestamp order."""
        db = InMemoryDB()
        
        # Put fields in non-lexicographic timestamp order
        db.put_at(300, "key1", "zebra", "value3")
        db.put_at(100, "key1", "apple", "value1")
        db.put_at(200, "key1", "banana", "value2")
        
        # Scan should return in lexicographic order
        result = db.scan_at(400, "key1")
        expected = ["apple(value1)", "banana(value2)", "zebra(value3)"]
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
