"""
Level 4 Unit Tests

Comprehensive test suite for the Level 4 backup and restore functionality.
Run with: python -m pytest test/test_level4.py -v
"""

import pytest
import sys
import os

# Add parent directory to path to import impl
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from impl import InMemoryDB


class TestInMemoryDBLevel4:
    """Test cases for Level 4 backup and restore methods of the InMemoryDB class."""
    
    def test_backup_at_basic(self):
        """Test basic backup functionality."""
        db = InMemoryDB()
        
        # Put some data
        db.put_at(100, "key1", "field1", "value1")
        db.put_at(100, "key1", "field2", "value2")
        
        # Backup at timestamp 120
        db.backup_at(120)
        
        # Add more data after backup
        db.put_at(130, "key1", "field3", "value3")
        
        # Restore should bring back the state at backup time
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        
        # Should have field1 and field2, but not field3
        assert db.get_at(200, "key1", "field1") == "value1"
        assert db.get_at(200, "key1", "field2") == "value2"
        assert db.get_at(200, "key1", "field3") is None
    
    def test_backup_at_with_ttl_entries(self):
        """Test backup includes TTL entries with remaining TTL."""
        db = InMemoryDB()
        
        # Put TTL entry at timestamp 100, expires at 150
        db.put_at_with_ttl(100, "key1", "session", "abc123", 50)
        
        # Backup at timestamp 120 (30 remaining TTL)
        db.backup_at(120)
        
        # Restore at timestamp 200
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        
        # Session should now expire at 200 + 30 = 230
        assert db.get_at(220, "key1", "session") == "abc123"  # Not expired
        assert db.get_at(230, "key1", "session") is None      # Expired
    
    def test_backup_at_excludes_expired_entries(self):
        """Test backup excludes expired entries."""
        db = InMemoryDB()
        
        # Put TTL entry that expires before backup
        db.put_at_with_ttl(100, "key1", "expired", "value1", 30)  # Expires at 130
        
        # Put permanent entry
        db.put_at(100, "key1", "permanent", "value2")
        
        # Backup at timestamp 140 (after expired entry expires)
        db.backup_at(140)
        
        # Restore
        db.restore_at(200, 140)  # Restore at timestamp 200, find closest backup <= 140
        
        # Only permanent entry should be restored
        assert db.get_at(200, "key1", "permanent") == "value2"
        assert db.get_at(200, "key1", "expired") is None
    
    def test_restore_at_closest_backup(self):
        """Test restore finds closest backup timestamp."""
        db = InMemoryDB()
        
        # Put initial data
        db.put_at(100, "key1", "field1", "value1")
        
        # Create multiple backups
        db.backup_at(120)
        db.put_at(130, "key1", "field2", "value2")
        db.backup_at(140)
        db.put_at(150, "key1", "field3", "value3")
        db.backup_at(160)
        
        # Restore to timestamp 125 (should use backup at 120)
        db.restore_at(125, 120)  # Restore at timestamp 125, find closest backup <= 120
        assert db.get_at(125, "key1", "field1") == "value1"
        assert db.get_at(125, "key1", "field2") is None
        assert db.get_at(125, "key1", "field3") is None
        
        # Restore to timestamp 135 (should use backup at 120)
        db.restore_at(135, 120)  # Restore at timestamp 135, find closest backup <= 120
        assert db.get_at(135, "key1", "field1") == "value1"
        assert db.get_at(135, "key1", "field2") is None
        
        # Restore to timestamp 145 (should use backup at 140)
        db.restore_at(145, 140)  # Restore at timestamp 145, find closest backup <= 140
        assert db.get_at(145, "key1", "field1") == "value1"
        assert db.get_at(145, "key1", "field2") == "value2"
        assert db.get_at(145, "key1", "field3") is None
    
    def test_restore_at_ttl_adjustment(self):
        """Test TTL adjustment during restore."""
        db = InMemoryDB()
        
        # Put TTL entry at timestamp 100, expires at 150
        db.put_at_with_ttl(100, "key1", "session", "abc123", 50)
        
        # Backup at timestamp 120 (30 remaining TTL)
        db.backup_at(120)
        
        # Restore at different timestamps and verify TTL adjustment
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        assert db.get_at(220, "key1", "session") == "abc123"  # Expires at 230
        assert db.get_at(230, "key1", "session") is None
        
        db.restore_at(300, 120)  # Restore at timestamp 300, find closest backup <= 120
        assert db.get_at(320, "key1", "session") == "abc123"  # Expires at 330
        assert db.get_at(330, "key1", "session") is None
    
    def test_backup_at_multiple_keys(self):
        """Test backup includes all keys."""
        db = InMemoryDB()
        
        # Put data for multiple keys
        db.put_at(100, "key1", "field1", "value1")
        db.put_at(100, "key2", "field1", "value2")
        db.put_at_with_ttl(100, "key1", "session", "abc123", 50)
        db.put_at_with_ttl(100, "key2", "session", "def456", 60)
        
        # Backup at timestamp 120
        db.backup_at(120)
        
        # Add more data
        db.put_at(130, "key1", "new_field", "new_value")
        db.put_at(130, "key3", "field1", "value3")
        
        # Restore
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        
        # Verify all keys from backup are restored
        assert db.get_at(200, "key1", "field1") == "value1"
        assert db.get_at(200, "key2", "field1") == "value2"
        assert db.get_at(200, "key1", "session") == "abc123"
        assert db.get_at(200, "key2", "session") == "def456"
        
        # Verify new data is not restored
        assert db.get_at(200, "key1", "new_field") is None
        assert db.get_at(200, "key3", "field1") is None
    
    def test_restore_at_replaces_current_state(self):
        """Test restore completely replaces current state."""
        db = InMemoryDB()
        
        # Initial state
        db.put_at(100, "key1", "field1", "value1")
        db.backup_at(120)
        
        # Modify state significantly
        db.put_at(130, "key1", "field1", "modified")
        db.put_at(130, "key1", "field2", "new_field")
        db.put_at(130, "key2", "field1", "new_key")
        db.delete_at(130, "key1", "field1")
        
        # Restore should completely replace current state
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        
        # Should be back to original state
        assert db.get_at(200, "key1", "field1") == "value1"
        assert db.get_at(200, "key1", "field2") is None
        assert db.get_at(200, "key2", "field1") is None
    
    def test_backup_at_empty_database(self):
        """Test backup of empty database."""
        db = InMemoryDB()
        
        # Backup empty database
        db.backup_at(100)
        
        # Add some data
        db.put_at(110, "key1", "field1", "value1")
        
        # Restore should result in empty database
        db.restore_at(200, 100)  # Restore at timestamp 200, find closest backup <= 100
        assert db.scan_at(200, "key1") == []
    
    def test_restore_at_no_backup(self):
        """Test restore when no backup exists."""
        db = InMemoryDB()
        
        # Put some data
        db.put_at(100, "key1", "field1", "value1")
        
        # Try to restore from non-existent backup
        db.restore_at(200, 50)  # Restore at timestamp 200, find closest backup <= 50
        
        # Database should be empty
        assert db.get_at(200, "key1", "field1") is None
    
    def test_backup_at_mixed_permanent_and_ttl(self):
        """Test backup with mix of permanent and TTL entries."""
        db = InMemoryDB()
        
        # Mix of entry types
        db.put_at(100, "key1", "permanent1", "value1")  # Permanent
        db.put_at_with_ttl(100, "key1", "ttl1", "value2", 50)  # Expires at 150
        db.put_at(100, "key1", "permanent2", "value3")  # Permanent
        db.put_at_with_ttl(100, "key1", "ttl2", "value4", 30)  # Expires at 130
        
        # Backup at timestamp 120
        db.backup_at(120)
        
        # Restore at timestamp 200
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        
        # Permanent entries should be restored as-is
        assert db.get_at(200, "key1", "permanent1") == "value1"
        assert db.get_at(200, "key1", "permanent2") == "value3"
        
        # TTL entries should be restored with adjusted expiry
        # ttl1: 30 remaining TTL -> expires at 200 + 30 = 230
        assert db.get_at(200, "key1", "ttl1") == "value2"
        assert db.get_at(220, "key1", "ttl1") == "value2"
        assert db.get_at(230, "key1", "ttl1") is None
        
        # ttl2: 10 remaining TTL -> expires at 200 + 10 = 210
        assert db.get_at(200, "key1", "ttl2") == "value4"
        assert db.get_at(210, "key1", "ttl2") is None
    
    def test_backup_at_scan_operations(self):
        """Test that scan operations work correctly after restore."""
        db = InMemoryDB()
        
        # Put multiple fields
        db.put_at(100, "key1", "apple", "value1")
        db.put_at(100, "key1", "banana", "value2")
        db.put_at_with_ttl(100, "key1", "cherry", "value3", 50)
        
        # Backup at timestamp 120
        db.backup_at(120)
        
        # Add more fields
        db.put_at(130, "key1", "date", "value4")
        
        # Restore
        db.restore_at(200, 120)  # Restore at timestamp 200, find closest backup <= 120
        
        # Test scan operations
        result = db.scan_at(200, "key1")
        expected = ["apple(value1)", "banana(value2)", "cherry(value3)"]
        assert result == expected
        
        result = db.scan_with_prefix_at(200, "key1", "a")
        assert result == ["apple(value1)"]
        
        # Test that new field is not included
        result = db.scan_at(200, "key1")
        assert "date(value4)" not in result
    
    def test_complex_backup_restore_scenario(self):
        """Test complex scenario with multiple backups and restores."""
        db = InMemoryDB()
        
        # Initial setup
        db.put_at(100, "user1", "name", "Alice")
        db.put_at_with_ttl(100, "user1", "session", "abc123", 100)  # Expires at 200
        
        # First backup at timestamp 120
        db.backup_at(120)
        
        # Add more data
        db.put_at(130, "user1", "email", "alice@example.com")
        db.put_at_with_ttl(130, "user1", "temp", "temp_value", 50)  # Expires at 180
        
        # Second backup at timestamp 140
        db.backup_at(140)
        
        # More changes
        db.put_at(150, "user1", "phone", "555-1234")
        db.delete_at(150, "user1", "name")
        
        # Restore to first backup
        db.restore_at(300, 120)  # Restore at timestamp 300, find closest backup <= 120
        
        # Verify state at timestamp 300
        assert db.get_at(300, "user1", "name") == "Alice"
        assert db.get_at(300, "user1", "email") is None  # Not in first backup
        assert db.get_at(300, "user1", "phone") is None  # Not in first backup
        assert db.get_at(300, "user1", "temp") is None    # Not in first backup
        
        # Session should have adjusted TTL: 80 remaining -> expires at 300 + 80 = 380
        assert db.get_at(300, "user1", "session") == "abc123"
        assert db.get_at(370, "user1", "session") == "abc123"
        assert db.get_at(380, "user1", "session") is None
        
        # Restore to second backup
        db.restore_at(400, 140)  # Restore at timestamp 400, find closest backup <= 140
        
        # Verify state at timestamp 400
        assert db.get_at(400, "user1", "name") == "Alice"
        assert db.get_at(400, "user1", "email") == "alice@example.com"
        assert db.get_at(400, "user1", "phone") is None  # Not in second backup
        
        # Temp should have adjusted TTL: 40 remaining -> expires at 400 + 40 = 440
        assert db.get_at(400, "user1", "temp") == "temp_value"
        assert db.get_at(430, "user1", "temp") == "temp_value"
        assert db.get_at(440, "user1", "temp") is None
        
        # Session should have adjusted TTL: 60 remaining -> expires at 400 + 60 = 460
        assert db.get_at(400, "user1", "session") == "abc123"
        assert db.get_at(450, "user1", "session") == "abc123"
        assert db.get_at(460, "user1", "session") is None
    
    def test_backup_at_edge_cases(self):
        """Test edge cases for backup operations."""
        db = InMemoryDB()
        
        # Test backup at exact expiration time
        db.put_at_with_ttl(100, "key1", "field1", "value1", 50)  # Expires at 150
        db.backup_at(150)  # Backup exactly at expiration
        
        # Entry should not be in backup
        db.restore_at(200, 150)  # Restore at timestamp 200, find closest backup <= 150
        assert db.get_at(200, "key1", "field1") is None
        
        # Test backup with zero TTL
        db.put_at_with_ttl(100, "key1", "field2", "value2", 0)  # Expires immediately
        db.backup_at(100)  # Backup at same timestamp
        
        # Entry should not be in backup
        db.restore_at(200, 100)  # Restore at timestamp 200, find closest backup <= 100
        assert db.get_at(200, "key1", "field2") is None
    
    def test_restore_at_edge_cases(self):
        """Test edge cases for restore operations."""
        db = InMemoryDB()
        
        # Test restore at same timestamp as backup
        db.put_at(100, "key1", "field1", "value1")
        db.backup_at(120)
        db.put_at(130, "key1", "field2", "value2")
        
        db.restore_at(120, 120)  # Restore at same timestamp
        assert db.get_at(120, "key1", "field1") == "value1"
        assert db.get_at(120, "key1", "field2") is None
        
        # Test restore with TTL adjustment to same timestamp
        db.put_at_with_ttl(100, "key1", "session", "abc123", 50)  # Expires at 150
        db.backup_at(120)  # 30 remaining TTL
        db.restore_at(120, 120)  # Restore at same timestamp
        
        # Should expire at 120 + 30 = 150
        assert db.get_at(120, "key1", "session") == "abc123"
        assert db.get_at(150, "key1", "session") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
