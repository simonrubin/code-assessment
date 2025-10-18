"""
In-Memory Database Implementation

This file contains the skeleton for implementing an in-memory database with 4 levels of complexity.
Complete the implementation of the InMemoryDB class to pass all tests.

Level 1: Basic CRUD operations
Level 2: Scanning and prefix filtering  
Level 3: Timestamp-based operations with TTL
Level 4: Backup and restore with TTL adjustment

Example usage:
    db = InMemoryDB()
    
    # Level 1 examples:
    db.put("user1", "name", "Alice")
    db.get("user1", "name")  # Returns "Alice"
    db.delete("user1", "name")  # Returns True
    
    # Level 2 examples:
    db.put("user1", "age", "25")
    db.put("user1", "address", "123 Main St")
    db.scan("user1")  # Returns ["address(123 Main St)", "age(25)"]
    db.scan_with_prefix("user1", "a")  # Returns ["address(123 Main St)", "age(25)"]
    
    # Level 3 examples:
    db.put_at(100, "user1", "temp_field", "temp_value")
    db.get_at(100, "user1", "temp_field")  # Returns "temp_value"
    db.put_at_with_ttl(100, "user1", "session", "abc123", 50)  # Expires at 150
    db.get_at(120, "user1", "session")  # Returns "abc123" (not expired)
    db.get_at(160, "user1", "session")  # Returns None (expired)
    db.delete_at(160, "user1", "session")  # Returns False (expired)
    
    # Level 4 examples:
    db.put_at_with_ttl(100, "user1", "session", "abc123", 50)  # Expires at 150
    db.backup_at(120)  # Backup with session having 30 remaining TTL
    db.put_at(130, "user1", "new_field", "new_value")  # Add new field
    db.restore_at(200, 120)  # Restore backup at timestamp 200, find closest backup <= 120
    # Session now expires at 200 + 30 = 230
    db.get_at(220, "user1", "session")  # Returns "abc123" (not expired)
    db.get_at(230, "user1", "session")  # Returns None (expired)
    db.get_at(200, "user1", "new_field")  # Returns None (not in backup)

Your implementation should pass all tests in test/test_level1.py, test/test_level2.py, test/test_level3.py, and test/test_level4.py
"""

from typing import Optional, List


class InMemoryDB:
    """
    An in-memory database that stores key-field-value mappings with advanced features.
    
    The database supports:
    - String keys that can map to multiple string fields
    - Each field maps to a single value
    - Timestamp-based operations with TTL support
    - Backup and restore functionality
    """
    
    def __init__(self):
        """Initialize an empty database."""
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 1 METHODS
    # ============================================================================
    
    def get(self, key: str, field: str) -> Optional[str]:
        """
        Retrieve the value for a given key and field.
        
        Args:
            key: The key to look up
            field: The field within that key
            
        Returns:
            The value if found, None otherwise
        """
        # TODO: Implement this method
        pass
    
    def put(self, key: str, field: str, value: str) -> None:
        """
        Store a value for a given key and field.
        
        Args:
            key: The key to store under
            field: The field within that key
            value: The value to store
        """
        # TODO: Implement this method
        pass
    
    def delete(self, key: str, field: str) -> bool:
        """
        Delete a field from a key.
        
        Args:
            key: The key containing the field
            field: The field to delete
            
        Returns:
            True if the field was deleted, False if it didn't exist
        """
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 2 METHODS
    # ============================================================================
    
    def scan(self, key: str) -> List[str]:
        """
        Return all fields for a given key in lexicographic order.
        
        Args:
            key: The key to scan
            
        Returns:
            List of strings in format ['field1(value1)', 'field2(value2)', ...]
            Returns empty list if key doesn't exist
        """
        # TODO: Implement this method
        pass
    
    def scan_with_prefix(self, key: str, prefix: str) -> List[str]:
        """
        Return fields for a given key that start with the specified prefix.
        
        Args:
            key: The key to scan
            prefix: The prefix to filter fields by
            
        Returns:
            List of strings in format ['field1(value1)', 'field2(value2)', ...]
            Only includes fields that start with prefix
            Returns empty list if key doesn't exist or no fields match prefix
        """
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 3 METHODS
    # ============================================================================
    
    def get_at(self, timestamp: int, key: str, field: str) -> Optional[str]:
        """
        Retrieve the value for a given key and field at a specific timestamp.
        
        Args:
            timestamp: The timestamp to query at
            key: The key to look up
            field: The field within that key
            
        Returns:
            The value if found and not expired, None otherwise
        """
        # TODO: Implement this method
        pass
    
    def put_at(self, timestamp: int, key: str, field: str, value: str) -> None:
        """
        Store a value for a given key and field at a specific timestamp.
        
        Args:
            timestamp: The timestamp to store at
            key: The key to store under
            field: The field within that key
            value: The value to store
        """
        # TODO: Implement this method
        pass
    
    def delete_at(self, timestamp: int, key: str, field: str) -> bool:
        """
        Delete a field from a key at a specific timestamp.
        
        Args:
            timestamp: The timestamp to delete at
            key: The key containing the field
            field: The field to delete
            
        Returns:
            True if the field was deleted, False if it didn't exist or was expired
        """
        # TODO: Implement this method
        pass
    
    def scan_at(self, timestamp: int, key: str) -> List[str]:
        """
        Return all fields for a given key in lexicographic order at a specific timestamp.
        
        Args:
            timestamp: The timestamp to scan at
            key: The key to scan
            
        Returns:
            List of strings in format ['field1(value1)', 'field2(value2)', ...]
            Only includes non-expired entries
            Returns empty list if key doesn't exist or all entries are expired
        """
        # TODO: Implement this method
        pass
    
    def scan_with_prefix_at(self, timestamp: int, key: str, prefix: str) -> List[str]:
        """
        Return fields for a given key that start with the specified prefix at a specific timestamp.
        
        Args:
            timestamp: The timestamp to scan at
            key: The key to scan
            prefix: The prefix to filter fields by
            
        Returns:
            List of strings in format ['field1(value1)', 'field2(value2)', ...]
            Only includes fields that start with prefix and are not expired
            Returns empty list if key doesn't exist or no fields match prefix
        """
        # TODO: Implement this method
        pass
    
    def put_at_with_ttl(self, timestamp: int, key: str, field: str, value: str, ttl: int) -> None:
        """
        Store a value for a given key and field at a specific timestamp with TTL.
        
        Args:
            timestamp: The timestamp to store at
            key: The key to store under
            field: The field within that key
            value: The value to store
            ttl: Time to live - entry expires at timestamp + ttl
        """
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 4 METHODS
    # ============================================================================
    
    def backup_at(self, timestamp: int) -> None:
        """
        Store a snapshot of the database at the given timestamp.
        
        Args:
            timestamp: The timestamp to create backup at
            
        Behavior:
            - Only non-expired entries are included in the backup
            - TTL entries store their remaining TTL at backup time
            - Permanent entries are stored as-is
        """
        # TODO: Implement this method
        pass
    
    def restore_at(self, timestamp: int, restore_at_timestamp: int) -> None:
        """
        Restore the database to the closest backup snapshot.
        
        Args:
            timestamp: The timestamp when restore_at is being called
            restore_at_timestamp: The timestamp to find the closest backup for
            
        Behavior:
            - Finds the closest backup timestamp <= restore_at_timestamp
            - Replaces current database state with backup state
            - Adjusts TTL entries: new_expiry = timestamp + remaining_ttl_at_backup
            - Permanent entries are restored as-is
        """
        # TODO: Implement this method
        pass