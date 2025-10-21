# Question 2: Shared Cloud File Storage

## Overview

Implement a shared cloud file storage system that stores file metadata in memory. The system maintains a mapping of filename to file metadata and provides methods to add, delete, and query files with increasing levels of complexity.

This is a scaffolding-based implementation where you need to complete the `FileStorage` class methods marked with `# TODO: Implement this method`.

## Level 1: Basic File Operations

### Problem Statement

You are tasked with implementing a shared cloud file storage system. The data structure will be implemented in memory. The file system stores a mapping of filename to file metadata (specifically file size).

### Requirements

Complete the implementation of the following methods in the `FileStorage` class:

1. **`add_file(name: str, size: int) -> bool`**
   - Returns `False` if the filename already exists
   - Returns `True` if successfully added to the file system
   - Stores the file with the given name and size

2. **`delete_file(name: str) -> bool`**
   - Returns `False` if the file does not exist
   - Otherwise removes the file from the file system and returns `True`

3. **`get_file_size(name: str) -> int | None`**
   - Returns `None` if the file does not exist
   - Otherwise returns the size of the file

## Level 2: File Size Querying

### Problem Statement

Extend the file storage system to support querying files by size. Implement functionality to retrieve the largest files in the system.

### Requirements

Complete the implementation of the following method in the `FileStorage` class:

4. **`get_largest_n(n: int) -> list[str]`**
   - Returns a list of the n largest files by size
   - Files are sorted by size (largest first)
   - In case of ties (same size), files are sorted alphabetically
   - Returns formatted strings in format `['filename1(size1)', 'filename2(size2)', ...]`
   - Returns empty list if no files exist or n <= 0

## Level 3: User Management

### Problem Statement

Extend the file storage system to support user management with storage capacity limits. Users can be added with specific storage allowances, and files can be added by specific users subject to their capacity constraints.

### Requirements

Complete the implementation of the following methods in the `FileStorage` class:

5. **`add_user(user_id: str, capacity: int) -> bool`**
   - Adds a user with the specified storage capacity
   - Returns `False` if the user already exists
   - Returns `True` if successfully added

6. **`add_file_by(user_id: str, name: str, size: int) -> int | None`**
   - Adds a file by a specific user
   - Returns `None` if user doesn't exist, file already exists, or would exceed capacity
   - Otherwise returns the remaining storage allowance for the user

7. **`merge_users(user_id_1: str, user_id_2: str) -> bool`**
   - Merges two users by reassigning all of user2's files to user1
   - User1 gets any unused storage held by user2
   - Deletes user2 after merging
   - Returns `False` if user_id_1 == user_id_2 or either user doesn't exist
   - Returns `True` if merge operation succeeds

## Level 4: Backup and Restore

### Problem Statement

Extend the file storage system to support backup and restore functionality for users. Users can create backups of their files at specific points in time and restore their files to those backup states.

### Requirements

Complete the implementation of the following methods in the `FileStorage` class:

8. **`backup(user_id: str) -> int | None`**
   - Creates a backup of the user's files at the current point in time
   - Returns the number of files backed up, `None` if user doesn't exist
   - At most one backup per user - subsequent backups overwrite previous ones

9. **`restore(user_id: str) -> int | None`**
   - Restores the user's files from their backup
   - Returns the number of files successfully restored, `None` if user doesn't exist
   - If a file exists and is owned by a different user, it cannot be restored
   - If backup is empty or doesn't exist, all user's files are deleted
   - Restore removes any present files not in the backup

### Additional Notes

- `delete_file()` should return storage allowance back to the file owner
- The original `add_file()` method is called by an "admin" user who has unlimited storage allowance
- Admin files and user files coexist in the same system

### Implementation Details

- Use an in-memory data structure to store the filename-to-metadata mapping
- File names are case-sensitive strings
- File sizes can be any integer (including zero and negative values)
- The system should handle edge cases like empty filenames and special characters
- Your implementation should be efficient and scalable

### Example Usage

```python
storage = FileStorage()

# Level 1: Basic operations
assert storage.add_file("document.txt", 1024) == True
assert storage.add_file("image.jpg", 2048) == True
assert storage.add_file("document.txt", 512) == False  # Duplicate name

# Query individual files
assert storage.get_file_size("document.txt") == 1024
assert storage.get_file_size("image.jpg") == 2048
assert storage.get_file_size("nonexistent.txt") == None

# Level 2: Size querying
storage.add_file("large.txt", 5000)
storage.add_file("medium.txt", 1000)
storage.add_file("small.txt", 500)

# Get largest files
assert storage.get_largest_n(2) == ["large.txt(5000)", "image.jpg(2048)"]
assert storage.get_largest_n(3) == ["large.txt(5000)", "image.jpg(2048)", "document.txt(1024)"]

# Level 3: User management
storage.add_user("alice", 5000)  # Alice gets 5000 bytes
storage.add_user("bob", 3000)    # Bob gets 3000 bytes

# Users add files within their capacity
remaining = storage.add_file_by("alice", "alice_doc.txt", 1000)  # Returns 4000
remaining = storage.add_file_by("bob", "bob_image.jpg", 2000)    # Returns 1000

# Merge users (Alice gets Bob's files and storage)
assert storage.merge_users("alice", "bob") == True

# Level 4: Backup and restore
storage.add_user("alice", 5000)
storage.add_file_by("alice", "doc1.txt", 1000)
storage.add_file_by("alice", "doc2.txt", 2000)
backup_count = storage.backup("alice")  # Returns 2 (files backed up)
storage.add_file_by("alice", "doc3.txt", 1500)  # Add more files
restore_count = storage.restore("alice")  # Returns 2 (files restored, doc3.txt removed)

# Delete files
assert storage.delete_file("document.txt") == True
assert storage.delete_file("document.txt") == False  # Already deleted
assert storage.get_file_size("document.txt") == None
```

### Test Cases

The test suite validates functionality without being implementation-specific:

**Level 1 Tests:**
- Basic add/delete/query operations
- Duplicate file handling
- Non-existent file operations
- Edge cases (empty filenames, zero sizes, large sizes, negative sizes)
- Special characters in filenames
- Case-sensitive filename handling
- Complete workflow scenarios

**Level 2 Tests:**
- Empty storage and edge cases (n <= 0)
- Single file and multiple files
- Size-based sorting with alphabetical tie-breaking
- Complex size patterns and ties
- Special characters and case-sensitive sorting
- File deletion impact on queries
- Format consistency validation

**Level 3 Tests:**
- User creation and duplicate handling
- File addition with capacity checking
- Capacity overflow prevention
- User merging and file reassignment
- Storage capacity return on file deletion
- Admin vs user file coexistence
- Edge cases (zero/negative capacity, large capacities)

**Level 4 Tests:**
- Backup creation and file counting
- Backup overwriting behavior
- Restore operations and file restoration
- File conflict resolution during restore
- Empty backup and no backup scenarios
- Capacity management during backup/restore
- Admin file isolation from user operations
- Multiple user backup/restore scenarios

## Structure

```
q2/
├── impl.py              # Your implementation goes here (scaffolding provided)
├── solution.py          # Complete working solution (reference only)
├── README.md           # This file - detailed requirements and examples
└── test/
    ├── __init__.py
    ├── test_level1.py   # Tests for Level 1
    ├── test_level2.py   # Tests for Level 2 (future)
    ├── test_level3.py   # Tests for Level 3 (future)
    └── test_level4.py   # Tests for Level 4 (future)
```

## Getting Started

1. Open `impl.py` and examine the scaffolding provided
2. Implement the `__init__` method to initialize your data structure
3. Implement the three Level 1 methods: `add_file`, `delete_file`, and `get_file_size`
4. Run the tests to verify your implementation

## Running Tests

To run the Level 1 tests:

```bash
cd q2
python -m pytest test/test_level1.py -v
```

To run all tests:

```bash
python -m pytest test/ -v
```

## Future Enhancements

The core functionality is now complete with all 4 levels implemented. Potential future enhancements could include:

- File versioning and history tracking
- Directory structure support
- File permissions and access control
- Advanced querying and filtering capabilities
- File sharing between users
- Compression and deduplication

## Tips

- Start with a simple data structure (like a dictionary) for Level 1
- For Level 2, consider efficient sorting algorithms for `get_largest_n`
- Use Python's built-in sorting with custom keys for size-based sorting with alphabetical tie-breaking
- For Level 3, track user capacity and file ownership in your data structures
- For Level 4, maintain backup snapshots that capture file ownership and metadata
- Consider how your Level 1 implementation will scale to future levels
- The tests are designed to validate functionality, not implementation details
- Focus on correctness first, then optimize for performance if needed
- For `get_largest_n`, you can use `sorted()` with a custom key function or `heapq.nlargest()`
- For user management, maintain separate tracking of user capacity and file ownership
- For backup/restore, consider deep copying file metadata to prevent reference issues
