# Coding Quiz - Level 1, 2, 3 & 4: In-Memory Database

## Overview
This is a 4-level coding quiz that builds progressively harder concepts. Each level focuses on different aspects of system design and implementation.

## Level 1 Requirements

Create an in-memory database class that supports the following operations:

### Database Structure
- The database takes **string keys**
- Each key may map to **multiple string fields**
- Each field may map to **only a single value**

### Required Methods
- `get(key: str, field: str) -> str | None` - Retrieve the value for a given key and field
- `delete(key: str, field: str) -> bool` - Delete a field from a key (returns True if deleted, False if not found)
- `put(key: str, field: str, value: str) -> None` - Store a value for a given key and field

## Level 2 Requirements

Add scanning capabilities to the database:

### Additional Methods
- `scan(key: str) -> List[str]` - Return all fields for a key in lexicographic order
  - Format: `['field1(value1)', 'field2(value2)', ...]`
- `scan_with_prefix(key: str, prefix: str) -> List[str]` - Return fields starting with prefix
  - Format: `['field1(value1)', 'field2(value2)', ...]` (only fields starting with prefix)

## Level 3 Requirements

Add timestamp-based operations with TTL (Time To Live) support:

### Timestamp-Based Methods
- `get_at(timestamp: int, key: str, field: str) -> str | None` - Get value at specific timestamp
- `put_at(timestamp: int, key: str, field: str, value: str) -> None` - Put value at specific timestamp
- `delete_at(timestamp: int, key: str, field: str) -> bool` - Delete field at specific timestamp
- `scan_at(timestamp: int, key: str) -> List[str]` - Scan all fields at specific timestamp
- `scan_with_prefix_at(timestamp: int, key: str, prefix: str) -> List[str]` - Scan with prefix at timestamp

### TTL Method
- `put_at_with_ttl(timestamp: int, key: str, field: str, value: str, ttl: int) -> None`
  - Entry expires at `timestamp + ttl`
  - Expired entries are ignored by all operations (return None/False/empty list)

### TTL Behavior
- Entries expire at `timestamp + ttl`
- Expired entries are ignored by all operations
- Non-timestamp methods operate at "current time" (implementation-defined)

## Level 4 Requirements

Add backup and restore functionality with TTL adjustment:

### Backup and Restore Methods
- `backup_at(timestamp: int) -> None` - Store a snapshot of the DB at the given timestamp
- `restore_at(timestamp: int, restore_at_timestamp: int) -> None` - Restore closest snapshot

### Backup Behavior
- Only non-expired entries are included in backups
- TTL entries store their remaining TTL at backup time
- Permanent entries are stored as-is

### Restore Behavior
- Finds the closest backup timestamp <= restore_at_timestamp
- Replaces current database state with backup state
- Adjusts TTL entries: `new_expiry = timestamp + remaining_ttl_at_backup`
- Permanent entries are restored as-is

### Example Usage
```python
db = InMemoryDB()
db.put("user1", "name", "Alice")
db.put("user1", "email", "alice@example.com")
db.get("user1", "name")  # Returns "Alice"
db.get("user1", "email")  # Returns "alice@example.com"
db.delete("user1", "email")  # Returns True
db.get("user1", "email")  # Returns None

    # Level 2 examples:
    db.put("user1", "age", "25")
    db.put("user1", "address", "123 Main St")
    db.scan("user1")  # Returns ['address(123 Main St)', 'age(25)', 'name(Alice)']
    db.scan_with_prefix("user1", "a")  # Returns ['address(123 Main St)', 'age(25)']
    
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
```

## Getting Started

1. **Read the requirements**: Check the requirements section above for detailed specifications
2. **Implement your solution**: Edit `impl.py` and implement the `InMemoryDB` class
3. **Run the tests**: Execute `python -m pytest test/test_level1.py -v` to verify your implementation
4. **All tests must pass**: Your implementation should pass all test cases

## Files
- `impl.py` - Your implementation file (edit this!)
- `test/test_level1.py` - Comprehensive test suite for Level 1
- `test/test_level2.py` - Comprehensive test suite for Level 2
- `test/test_level3.py` - Comprehensive test suite for Level 3
- `test/test_level4.py` - Comprehensive test suite for Level 4
- `README.md` - This file

## Testing
Run the tests with:
```bash
# Test Level 1 only
python -m pytest test/test_level1.py -v

# Test Level 2 only
python -m pytest test/test_level2.py -v

# Test Level 3 only
python -m pytest test/test_level3.py -v

# Test Level 4 only
python -m pytest test/test_level4.py -v

# Test all levels
python -m pytest test/ -v
```

Or run individual test methods:
```bash
python -m pytest test/test_level1.py::TestInMemoryDB::test_basic_put_and_get -v
python -m pytest test/test_level2.py::TestInMemoryDBLevel2::test_scan_multiple_fields_lexicographic_order -v
python -m pytest test/test_level3.py::TestInMemoryDBLevel3::test_put_at_with_ttl_basic -v
python -m pytest test/test_level4.py::TestInMemoryDBLevel4::test_backup_at_with_ttl_entries -v
```

## Success Criteria
- All tests in `test/test_level1.py` must pass (Level 1)
- All tests in `test/test_level2.py` must pass (Level 2)
- All tests in `test/test_level3.py` must pass (Level 3)
- All tests in `test/test_level4.py` must pass (Level 4)
- Your implementation should handle edge cases (empty strings, non-existent keys/fields, TTL expiration, backup/restore)
- The code should be clean and well-structured
- Fields must be returned in lexicographic order for scan methods
- TTL expiration must be handled correctly for all operations
- Backup and restore must correctly adjust TTL values

## Next Steps
Congratulations! You've completed all 4 levels of the coding quiz. This comprehensive implementation covers:

- **Level 1**: Basic CRUD operations
- **Level 2**: Scanning and prefix filtering  
- **Level 3**: Timestamp-based operations with TTL
- **Level 4**: Backup and restore with TTL adjustment

This represents a complete in-memory database system with advanced features!

Good luck! 🚀
