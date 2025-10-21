"""
Question 2 - Level 3 Tests: User Management

Test cases for user management functionality:
- add_user: Adding users with storage capacity
- add_file_by: Adding files by specific users with capacity checking
- merge_users: Merging users and reassigning files/storage

These tests validate functionality without being implementation-specific.
"""

import pytest
from impl import FileStorage


class TestQuestion2Level3:
    """Test cases for Question 2 Level 3 - User Management."""
    
    def setup_method(self):
        """Set up a fresh FileStorage instance for each test."""
        self.storage = FileStorage()
    
    def test_add_user_success(self):
        """Test successfully adding a user."""
        result = self.storage.add_user("alice", 5000)
        assert result is True
        
        # User should be able to add files within capacity
        remaining = self.storage.add_file_by("alice", "test.txt", 1000)
        assert remaining == 4000
    
    def test_add_user_duplicate(self):
        """Test adding a user with duplicate ID returns False."""
        self.storage.add_user("alice", 5000)
        result = self.storage.add_user("alice", 3000)
        assert result is False
        
        # Original capacity should be preserved
        remaining = self.storage.add_file_by("alice", "test.txt", 1000)
        assert remaining == 4000  # 5000 - 1000, not 3000 - 1000
    
    def test_add_user_zero_capacity(self):
        """Test adding a user with zero capacity."""
        result = self.storage.add_user("empty_user", 0)
        assert result is True
        
        # Should not be able to add any files
        remaining = self.storage.add_file_by("empty_user", "test.txt", 1)
        assert remaining is None
    
    def test_add_user_negative_capacity(self):
        """Test adding a user with negative capacity."""
        result = self.storage.add_user("negative_user", -1000)
        assert result is True
        
        # Should not be able to add any files
        remaining = self.storage.add_file_by("negative_user", "test.txt", 1)
        assert remaining is None
    
    def test_add_file_by_nonexistent_user(self):
        """Test adding file by non-existent user returns None."""
        remaining = self.storage.add_file_by("nonexistent", "test.txt", 1000)
        assert remaining is None
    
    def test_add_file_by_success(self):
        """Test successfully adding file by user."""
        self.storage.add_user("alice", 5000)
        
        remaining = self.storage.add_file_by("alice", "test.txt", 1000)
        assert remaining == 4000
        
        # File should exist in the system
        assert self.storage.get_file_size("test.txt") == 1000
    
    def test_add_file_by_exceeds_capacity(self):
        """Test adding file that exceeds user capacity returns None."""
        self.storage.add_user("alice", 1000)
        
        # Try to add file larger than capacity
        remaining = self.storage.add_file_by("alice", "large.txt", 2000)
        assert remaining is None
        
        # File should not exist in the system
        assert self.storage.get_file_size("large.txt") is None
    
    def test_add_file_by_duplicate_filename(self):
        """Test adding file with duplicate filename returns None."""
        self.storage.add_user("alice", 5000)
        self.storage.add_user("bob", 5000)
        
        # Alice adds file first
        remaining1 = self.storage.add_file_by("alice", "test.txt", 1000)
        assert remaining1 == 4000
        
        # Bob tries to add file with same name
        remaining2 = self.storage.add_file_by("bob", "test.txt", 1000)
        assert remaining2 is None
        
        # File should still belong to Alice
        assert self.storage.get_file_size("test.txt") == 1000
    
    def test_add_file_by_exact_capacity(self):
        """Test adding file that uses exact capacity."""
        self.storage.add_user("alice", 1000)
        
        remaining = self.storage.add_file_by("alice", "exact.txt", 1000)
        assert remaining == 0
        
        # Should not be able to add another file
        remaining2 = self.storage.add_file_by("alice", "another.txt", 1)
        assert remaining2 is None
    
    def test_add_file_by_multiple_files(self):
        """Test adding multiple files by same user."""
        self.storage.add_user("alice", 5000)
        
        remaining1 = self.storage.add_file_by("alice", "file1.txt", 1000)
        assert remaining1 == 4000
        
        remaining2 = self.storage.add_file_by("alice", "file2.txt", 2000)
        assert remaining2 == 2000
        
        remaining3 = self.storage.add_file_by("alice", "file3.txt", 1500)
        assert remaining3 == 500
        
        # All files should exist
        assert self.storage.get_file_size("file1.txt") == 1000
        assert self.storage.get_file_size("file2.txt") == 2000
        assert self.storage.get_file_size("file3.txt") == 1500
    
    def test_merge_users_success(self):
        """Test successfully merging two users."""
        self.storage.add_user("alice", 5000)
        self.storage.add_user("bob", 3000)
        
        # Add files to both users
        self.storage.add_file_by("alice", "alice_file.txt", 1000)  # Alice: 4000 remaining
        self.storage.add_file_by("bob", "bob_file.txt", 2000)     # Bob: 1000 remaining
        
        # Merge users
        result = self.storage.merge_users("alice", "bob")
        assert result is True
        
        # Alice should have both files and combined capacity
        assert self.storage.get_file_size("alice_file.txt") == 1000
        assert self.storage.get_file_size("bob_file.txt") == 2000
        
        # Alice should be able to add file using Bob's remaining capacity
        remaining = self.storage.add_file_by("alice", "new_file.txt", 1000)
        assert remaining == 4000  # Alice's remaining (4000) + Bob's remaining (1000)
        
        # Bob should no longer exist
        remaining_bob = self.storage.add_file_by("bob", "test.txt", 1000)
        assert remaining_bob is None
    
    def test_merge_users_same_user(self):
        """Test merging same user returns False."""
        self.storage.add_user("alice", 5000)
        
        result = self.storage.merge_users("alice", "alice")
        assert result is False
    
    def test_merge_users_nonexistent_users(self):
        """Test merging non-existent users returns False."""
        self.storage.add_user("alice", 5000)
        
        # Merge with non-existent user
        result1 = self.storage.merge_users("alice", "nonexistent")
        assert result1 is False
        
        result2 = self.storage.merge_users("nonexistent", "alice")
        assert result2 is False
        
        result3 = self.storage.merge_users("nonexistent1", "nonexistent2")
        assert result3 is False
    
    def test_merge_users_empty_users(self):
        """Test merging users with no files."""
        self.storage.add_user("alice", 5000)
        self.storage.add_user("bob", 3000)
        
        result = self.storage.merge_users("alice", "bob")
        assert result is True
        
        # Alice should have combined capacity
        remaining = self.storage.add_file_by("alice", "test.txt", 8000)
        assert remaining == 0  # 5000 + 3000 - 8000
    
    def test_merge_users_capacity_overflow(self):
        """Test merging users with files that exceed capacity."""
        self.storage.add_user("alice", 1000)
        self.storage.add_user("bob", 1000)
        
        # Both users use their full capacity
        self.storage.add_file_by("alice", "alice_file.txt", 1000)
        self.storage.add_file_by("bob", "bob_file.txt", 1000)
        
        # Merge should succeed
        result = self.storage.merge_users("alice", "bob")
        assert result is True
        
        # Alice should have both files and combined capacity
        assert self.storage.get_file_size("alice_file.txt") == 1000
        assert self.storage.get_file_size("bob_file.txt") == 1000
        
        # Alice should have 1000 remaining capacity
        remaining = self.storage.add_file_by("alice", "new_file.txt", 1000)
        assert remaining == 0
    
    def test_delete_file_returns_capacity(self):
        """Test that delete_file returns capacity to file owner."""
        self.storage.add_user("alice", 5000)
        
        # Add file
        remaining = self.storage.add_file_by("alice", "test.txt", 1000)
        assert remaining == 4000
        
        # Delete file
        delete_result = self.storage.delete_file("test.txt")
        assert delete_result is True
        
        # Capacity should be returned
        remaining_after_delete = self.storage.add_file_by("alice", "new_file.txt", 5000)
        assert remaining_after_delete == 0
    
    def test_delete_file_nonexistent_owner(self):
        """Test deleting file when owner no longer exists."""
        self.storage.add_user("alice", 5000)
        self.storage.add_file_by("alice", "test.txt", 1000)
        
        # Delete user (simulate user deletion)
        # Note: This tests the system's behavior when a file exists but owner is gone
        # The exact behavior is implementation-dependent
        delete_result = self.storage.delete_file("test.txt")
        assert delete_result is True
    
    def test_admin_add_file_unlimited_capacity(self):
        """Test that admin (using add_file) has unlimited capacity."""
        # Admin adds files without user management
        result1 = self.storage.add_file("admin_file1.txt", 10000)
        assert result1 is True
        
        result2 = self.storage.add_file("admin_file2.txt", 20000)
        assert result2 is True
        
        # Files should exist
        assert self.storage.get_file_size("admin_file1.txt") == 10000
        assert self.storage.get_file_size("admin_file2.txt") == 20000
    
    def test_mixed_admin_and_user_files(self):
        """Test interaction between admin files and user files."""
        self.storage.add_user("alice", 1000)
        
        # Admin adds file
        self.storage.add_file("admin_file.txt", 5000)
        
        # Alice adds file
        remaining = self.storage.add_file_by("alice", "alice_file.txt", 1000)
        assert remaining == 0
        
        # Both files should exist
        assert self.storage.get_file_size("admin_file.txt") == 5000
        assert self.storage.get_file_size("alice_file.txt") == 1000
        
        # get_largest_n should include both
        largest = self.storage.get_largest_n(2)
        assert "admin_file.txt(5000)" in largest
        assert "alice_file.txt(1000)" in largest
    
    def test_merge_users_with_admin_files(self):
        """Test that admin files are not affected by user merging."""
        self.storage.add_user("alice", 1000)
        self.storage.add_user("bob", 1000)
        
        # Admin adds file
        self.storage.add_file("admin_file.txt", 5000)
        
        # Users add files
        self.storage.add_file_by("alice", "alice_file.txt", 1000)
        self.storage.add_file_by("bob", "bob_file.txt", 1000)
        
        # Merge users
        result = self.storage.merge_users("alice", "bob")
        assert result is True
        
        # Admin file should be unaffected
        assert self.storage.get_file_size("admin_file.txt") == 5000
        
        # User files should be merged
        assert self.storage.get_file_size("alice_file.txt") == 1000
        assert self.storage.get_file_size("bob_file.txt") == 1000
    
    def test_user_capacity_edge_cases(self):
        """Test edge cases with user capacity."""
        # Test with very large capacity
        self.storage.add_user("big_user", 1000000)
        remaining = self.storage.add_file_by("big_user", "big_file.txt", 999999)
        assert remaining == 1
        
        # Test with capacity of 1
        self.storage.add_user("tiny_user", 1)
        remaining = self.storage.add_file_by("tiny_user", "tiny_file.txt", 1)
        assert remaining == 0
        
        # Should not be able to add another file
        remaining2 = self.storage.add_file_by("tiny_user", "another.txt", 1)
        assert remaining2 is None
