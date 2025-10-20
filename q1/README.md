# Question 1: In-Memory Database

This question asks you to implement an in-memory database with 4 levels of complexity.

## Overview

Implement an `InMemoryDB` class that stores key-field-value mappings with advanced features including timestamp-based operations, TTL support, and backup/restore functionality.

## Requirements

### Level 1: Basic CRUD Operations
- `get(key, field) -> Optional[str]` - Retrieve a value
- `put(key, field, value)` - Store a value  
- `delete(key, field) -> bool` - Delete a field

### Level 2: Scanning and Prefix Filtering
- `scan(key) -> List[str]` - Return all fields in lexicographic order
- `scan_with_prefix(key, prefix) -> List[str]` - Filter by prefix

### Level 3: Timestamp-based Operations with TTL
- All previous methods with `_at(timestamp, ...)` variants
- `put_at_with_ttl(timestamp, key, field, value, ttl)` - Store with expiration
- Proper versioning and temporal logic

### Level 4: Backup and Restore with TTL Adjustment
- `backup_at(timestamp)` - Store database snapshot
- `restore_at(timestamp, restore_at_timestamp)` - Restore with TTL adjustment

## Example Usage

```python
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
3. **Test your implementation**: Run the tests to verify your solution

## Testing

Run tests for each level:

```bash
# Test Level 1
python -m pytest test/test_level1.py -v

# Test Level 2  
python -m pytest test/test_level2.py -v

# Test Level 3
python -m pytest test/test_level3.py -v

# Test Level 4
python -m pytest test/test_level4.py -v

# Test all levels
python -m pytest test/ -v
```

## File Structure

```
q1/
├── impl.py              # Your implementation goes here
├── solution.py          # Complete working solution (reference only)
└── test/
    ├── __init__.py
    ├── test_level1.py   # 11 tests for Level 1
    ├── test_level2.py   # 18 tests for Level 2  
    ├── test_level3.py   # 18 tests for Level 3
    └── test_level4.py   # 18 tests for Level 4
```

## Success Criteria

- All tests pass for each level
- Implementation handles edge cases correctly
- Code is clean and well-structured
- Proper error handling for invalid inputs
