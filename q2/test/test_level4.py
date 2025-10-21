"""
Question 2 - Level 4 Tests: Backup and Restore

Test cases for backup and restore functionality:
- backup: Creating backups of user files
- restore: Restoring user files from backups

These tests validate functionality without being implementation-specific.
"""

import pytest
from impl import FileStorage


class TestQuestion2Level4:
    """Test cases for Question 2 Level 4 - Backup and Restore."""
    
    def setup_method(self):
        """Set up a fresh FileStorage instance for each test."""
        self.storage = FileStorage()
    
    def test_backup_nonexistent_user(self):
        """Test backup of non-existent user returns None."""
        result = self.storage.backup("nonexistent")
        assert result is None
    
    def test_backup_user_with_no_files(self):
        """Test backup of user with no files returns 0."""
        self.storage.add_user("alice", 5000)
        
        result = self.storage.backup("alice")
        assert result == 0
    
    def test_backup_user_with_files(self):
        """Test backup of user with files returns correct count."""
        self.storage.add_user("alice", 5000)
        self.storage.add_file_by("alice", "file1.txt", 1000)
        self.storage.add_file_by("alice", "file2.txt", 2000)
        self.storage.add_file_by("alice", "file3.txt", 1500)
        
        result = self.storage.backup("alice")
        assert result == 3
    
    def test_backup_overwrites_previous(self):
        """Test that subsequent backups overwrite previous ones."""
        self.storage.add_user("alice", 5000)
        
        # First backup
        self.storage.add_file_by("alice", "file1.txt", 1000)
        result1 = self.storage.backup("alice")
        assert result1 == 1
        
        # Add more files and backup again
        self.storage.add_file_by("alice", "file2.txt", 2000)
        self.storage.add_file_by("alice", "file3.txt", 1500)
        result2 = self.storage.backup("alice")
        assert result2 == 3
        
        # Restore should only restore the latest backup
        restore_count = self.storage.restore("alice")
        assert restore_count == 3
        assert self.storage.get_file_size("file1.txt") == 1000
        assert self.storage.get_file_size("file2.txt") == 2000
        assert self.storage.get_file_size("file3.txt") == 1500
    
    def test_restore_nonexistent_user(self):
        """Test restore of non-existent user returns None."""
        result = self.storage.restore("nonexistent")
        assert result is None
    
    def test_restore_user_with_no_backup(self):
        """Test restore of user with no backup deletes all files."""
        self.storage.add_user("alice", 5000)
        self.storage.add_file_by("alice", "file1.txt", 1000)
        self.storage.add_file_by("alice", "file2.txt", 2000)
        
        # Restore without backup should delete all files
        result = self.storage.restore("alice")
        assert result == 0
        
        # All files should be deleted
        assert self.storage.get_file_size("file1.txt") is None
        assert self.storage.get_file_size("file2.txt") is None
    
    def test_restore_user_with_empty_backup(self):
        """Test restore of user with empty backup deletes all files."""
        self.storage.add_user("alice", 5000)
        
        # Create empty backup
        self.storage.backup("alice")  # Should return 0
        
        # Add files after backup
        self.storage.add_file_by("alice", "file1.txt", 1000)
        self.storage.add_file_by("alice", "file2.txt", 2000)
        
        # Restore should delete all files
        result = self.storage.restore("alice")
        assert result == 0
        
        # All files should be deleted
        assert self.storage.get_file_size("file1.txt") is None
        assert self.storage.get_file_size("file2.txt") is None
    
    def test_restore_successful(self):
        """Test successful restore operation."""
        self.storage.add_user("alice", 5000)
        
        # Add files and backup
        self.storage.add_file_by("alice", "file1.txt", 1000)
        self.storage.add_file_by("alice", "file2.txt", 2000)
        backup_count = self.storage.backup("alice")
        assert backup_count == 2
        
        # Add more files after backup
        self.storage.add_file_by("alice", "file3.txt", 1500)
        self.storage.add_file_by("alice", "file4.txt", 500)
        
        # Restore should return files to backup state
        restore_count = self.storage.restore("alice")
        assert restore_count == 2
        
        # Only backup files should exist
        assert self.storage.get_file_size("file1.txt") == 1000
        assert self.storage.get_file_size("file2.txt") == 2000
        assert self.storage.get_file_size("file3.txt") is None
        assert self.storage.get_file_size("file4.txt") is None
    
    def test_restore_with_file_conflicts(self):
        """Test restore when files exist and are owned by different users."""
        self.storage.add_user("alice", 5000)
        self.storage.add_user("bob", 5000)
        
        # Alice adds files and backs up
        self.storage.add_file_by("alice", "file1.txt", 1000)
        self.storage.add_file_by("alice", "file2.txt", 2000)
        backup_count = self.storage.backup("alice")
        assert backup_count == 2
        
        # Alice deletes file2.txt after backup
        self.storage.delete_file("file2.txt")
        
        # Bob adds file with same name as Alice's deleted file
        self.storage.add_file_by("bob", "file2.txt", 1500)
        
        # Alice adds more files after backup
        self.storage.add_file_by("alice", "new_file.txt", 1000)
        
        # Restore Alice - file2.txt cannot be restored due to conflict with Bob's file
        restore_count = self.storage.restore("alice")
        assert restore_count == 1  # Only file1.txt restored
        
        # Check file states
        assert self.storage.get_file_size("file1.txt") == 1000  # Restored
        assert self.storage.get_file_size("file2.txt") == 1500  # Bob's version (conflict)
        assert self.storage.get_file_size("new_file.txt") is None  # Removed
    
    def test_restore_removes_extra_files(self):
        """Test that restore removes files not in backup."""
        self.storage.add_user("alice", 5000)
        
        # Add files and backup
        self.storage.add_file_by("alice", "keep1.txt", 1000)
        self.storage.add_file_by("alice", "keep2.txt", 2000)
        self.storage.backup("alice")
        
        # Add more files after backup
        self.storage.add_file_by("alice", "remove1.txt", 1500)
        self.storage.add_file_by("alice", "remove2.txt", 500)
        
        # Restore
        restore_count = self.storage.restore("alice")
        assert restore_count == 2
        
        # Only backup files should remain
        assert self.storage.get_file_size("keep1.txt") == 1000
        assert self.storage.get_file_size("keep2.txt") == 2000
        assert self.storage.get_file_size("remove1.txt") is None
        assert self.storage.get_file_size("remove2.txt") is None
    
    def test_backup_restore_capacity_management(self):
        """Test that backup/restore properly manages user capacity."""
        self.storage.add_user("alice", 5000)
        
        # Add files and backup
        self.storage.add_file_by("alice", "file1.txt", 1000)
        self.storage.add_file_by("alice", "file2.txt", 2000)
        self.storage.backup("alice")
        
        # Add more files (uses remaining capacity)
        remaining = self.storage.add_file_by("alice", "file3.txt", 2000)
        assert remaining == 0  # Should use all capacity
        
        # Restore should free up capacity (file3.txt is removed, freeing 2000)
        self.storage.restore("alice")
        
        # Should be able to add files again (2000 capacity available)
        remaining_after_restore = self.storage.add_file_by("alice", "new_file.txt", 2000)
        assert remaining_after_restore == 0  # 5000 - 1000 - 2000 - 2000 = 0 remaining
    
    def test_backup_restore_with_admin_files(self):
        """Test that backup/restore doesn't affect admin files."""
        self.storage.add_user("alice", 5000)
        
        # Admin adds file
        self.storage.add_file("admin_file.txt", 10000)
        
        # Alice adds files and backs up
        self.storage.add_file_by("alice", "alice_file.txt", 1000)
        self.storage.backup("alice")
        
        # Alice adds more files
        self.storage.add_file_by("alice", "alice_file2.txt", 2000)
        
        # Restore Alice
        self.storage.restore("alice")
        
        # Admin file should be unaffected
        assert self.storage.get_file_size("admin_file.txt") == 10000
        assert self.storage.get_file_size("alice_file.txt") == 1000
        assert self.storage.get_file_size("alice_file2.txt") is None
    
    def test_backup_restore_multiple_users(self):
        """Test backup/restore with multiple users."""
        self.storage.add_user("alice", 5000)
        self.storage.add_user("bob", 3000)
        
        # Both users add files
        self.storage.add_file_by("alice", "alice1.txt", 1000)
        self.storage.add_file_by("alice", "alice2.txt", 2000)
        self.storage.add_file_by("bob", "bob1.txt", 1500)
        
        # Alice backs up
        alice_backup = self.storage.backup("alice")
        assert alice_backup == 2
        
        # Bob backs up
        bob_backup = self.storage.backup("bob")
        assert bob_backup == 1
        
        # Both users add more files
        self.storage.add_file_by("alice", "alice3.txt", 2000)
        self.storage.add_file_by("bob", "bob2.txt", 1000)
        
        # Restore Alice
        alice_restore = self.storage.restore("alice")
        assert alice_restore == 2
        
        # Restore Bob
        bob_restore = self.storage.restore("bob")
        assert bob_restore == 1
        
        # Check final state
        assert self.storage.get_file_size("alice1.txt") == 1000
        assert self.storage.get_file_size("alice2.txt") == 2000
        assert self.storage.get_file_size("alice3.txt") is None
        assert self.storage.get_file_size("bob1.txt") == 1500
        assert self.storage.get_file_size("bob2.txt") is None
        
    def test_backup_restore_special_filenames(self):
        """Test backup/restore with special characters in filenames."""
        self.storage.add_user("alice", 5000)
        
        special_files = [
            "file with spaces.txt",
            "file-with-dashes.txt",
            "file_with_underscores.txt",
            "file.with.dots.txt"
        ]
        
        for filename in special_files:
            self.storage.add_file_by("alice", filename, 1000)
        
        backup_count = self.storage.backup("alice")
        assert backup_count == 4
        
        # Add more files
        self.storage.add_file_by("alice", "extra.txt", 1000)
        
        # Restore
        restore_count = self.storage.restore("alice")
        assert restore_count == 4
        
        # Check all special files are restored
        for filename in special_files:
            assert self.storage.get_file_size(filename) == 1000
        
        # Extra file should be removed
        assert self.storage.get_file_size("extra.txt") is None
    
    def test_backup_restore_after_user_merge(self):
        """Test backup/restore after users have been merged."""
        self.storage.add_user("alice", 5000)
        self.storage.add_user("bob", 3000)
        
        # Both users add files
        self.storage.add_file_by("alice", "alice_file.txt", 1000)
        self.storage.add_file_by("bob", "bob_file.txt", 2000)
        
        # Alice backs up before merge
        alice_backup = self.storage.backup("alice")
        assert alice_backup == 1
        
        # Merge users
        self.storage.merge_users("alice", "bob")
        
        # Alice should have both files now
        assert self.storage.get_file_size("alice_file.txt") == 1000
        assert self.storage.get_file_size("bob_file.txt") == 2000
        
        # Restore Alice should only restore her original file
        restore_count = self.storage.restore("alice")
        assert restore_count == 1
        
        assert self.storage.get_file_size("alice_file.txt") == 1000
        assert self.storage.get_file_size("bob_file.txt") is None  # Not in Alice's backup
