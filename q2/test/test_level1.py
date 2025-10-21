"""
Question 2 - Level 1 Tests: Shared Cloud File Storage

Test cases for the basic file storage operations:
- add_file: Adding files to storage
- delete_file: Removing files from storage  
- get_file_size: Querying file sizes

These tests validate functionality without being implementation-specific.
"""

import pytest
from impl import FileStorage


class TestQuestion2Level1:
    """Test cases for Question 2 Level 1 - Basic File Storage Operations."""
    
    def setup_method(self):
        """Set up a fresh FileStorage instance for each test."""
        self.storage = FileStorage()
    
    def test_add_file_success(self):
        """Test successfully adding a file."""
        result = self.storage.add_file("test.txt", 1024)
        assert result is True
        assert self.storage.get_file_size("test.txt") == 1024
    
    def test_add_file_duplicate(self):
        """Test adding a file with duplicate name returns False."""
        # Add file first time
        result1 = self.storage.add_file("duplicate.txt", 512)
        assert result1 is True
        
        # Try to add same file again
        result2 = self.storage.add_file("duplicate.txt", 1024)
        assert result2 is False
        
        # Original size should be preserved
        assert self.storage.get_file_size("duplicate.txt") == 512
    
    def test_add_file_zero_size(self):
        """Test adding a file with zero size."""
        result = self.storage.add_file("empty.txt", 0)
        assert result is True
        assert self.storage.get_file_size("empty.txt") == 0
    
    def test_add_file_large_size(self):
        """Test adding a file with large size."""
        large_size = 1024 * 1024 * 1024  # 1GB
        result = self.storage.add_file("large.bin", large_size)
        assert result is True
        assert self.storage.get_file_size("large.bin") == large_size
    
    def test_add_multiple_files(self):
        """Test adding multiple different files."""
        files = [
            ("file1.txt", 100),
            ("file2.txt", 200),
            ("file3.txt", 300)
        ]
        
        for name, size in files:
            result = self.storage.add_file(name, size)
            assert result is True
            assert self.storage.get_file_size(name) == size
    
    def test_delete_file_success(self):
        """Test successfully deleting a file."""
        # Add file first
        self.storage.add_file("to_delete.txt", 256)
        assert self.storage.get_file_size("to_delete.txt") == 256
        
        # Delete file
        result = self.storage.delete_file("to_delete.txt")
        assert result is True
        
        # File should no longer exist
        assert self.storage.get_file_size("to_delete.txt") is None
    
    def test_delete_file_nonexistent(self):
        """Test deleting a file that doesn't exist returns False."""
        result = self.storage.delete_file("nonexistent.txt")
        assert result is False
    
    def test_delete_file_empty_storage(self):
        """Test deleting from empty storage."""
        result = self.storage.delete_file("any_file.txt")
        assert result is False
    
    def test_get_file_size_existing(self):
        """Test getting size of existing file."""
        self.storage.add_file("existing.txt", 1024)
        size = self.storage.get_file_size("existing.txt")
        assert size == 1024
    
    def test_get_file_size_nonexistent(self):
        """Test getting size of non-existent file returns None."""
        size = self.storage.get_file_size("nonexistent.txt")
        assert size is None
    
    def test_get_file_size_empty_storage(self):
        """Test getting size from empty storage."""
        size = self.storage.get_file_size("any_file.txt")
        assert size is None
    
    def test_complete_workflow(self):
        """Test complete workflow: add, query, delete, query."""
        # Add file
        add_result = self.storage.add_file("workflow.txt", 2048)
        assert add_result is True
        
        # Query file
        size = self.storage.get_file_size("workflow.txt")
        assert size == 2048
        
        # Delete file
        delete_result = self.storage.delete_file("workflow.txt")
        assert delete_result is True
        
        # Query deleted file
        size_after_delete = self.storage.get_file_size("workflow.txt")
        assert size_after_delete is None
    
    def test_add_after_delete(self):
        """Test adding a file with same name after deletion."""
        # Add file
        self.storage.add_file("recycled.txt", 100)
        assert self.storage.get_file_size("recycled.txt") == 100
        
        # Delete file
        self.storage.delete_file("recycled.txt")
        assert self.storage.get_file_size("recycled.txt") is None
        
        # Add file with same name but different size
        result = self.storage.add_file("recycled.txt", 200)
        assert result is True
        assert self.storage.get_file_size("recycled.txt") == 200
    
    def test_special_characters_in_filename(self):
        """Test files with special characters in names."""
        special_names = [
            "file with spaces.txt",
            "file-with-dashes.txt", 
            "file_with_underscores.txt",
            "file.with.dots.txt",
            "file123.txt"
        ]
        
        for i, name in enumerate(special_names):
            result = self.storage.add_file(name, 100 + i)
            assert result is True
            assert self.storage.get_file_size(name) == 100 + i
    
    def test_empty_filename(self):
        """Test behavior with empty filename."""
        result = self.storage.add_file("", 100)
        assert result is True
        assert self.storage.get_file_size("") == 100
        
        # Should be able to delete empty filename
        delete_result = self.storage.delete_file("")
        assert delete_result is True
        assert self.storage.get_file_size("") is None
    
    def test_negative_size_handling(self):
        """Test behavior with negative file sizes."""
        # Implementation should handle negative sizes gracefully
        # This test validates the behavior without prescribing implementation
        result = self.storage.add_file("negative.txt", -100)
        # The exact behavior is implementation-dependent
        # but should be consistent
        if result:
            size = self.storage.get_file_size("negative.txt")
            assert size == -100
    
    def test_case_sensitive_filenames(self):
        """Test that filenames are case-sensitive."""
        self.storage.add_file("File.txt", 100)
        self.storage.add_file("file.txt", 200)
        self.storage.add_file("FILE.txt", 300)
        
        assert self.storage.get_file_size("File.txt") == 100
        assert self.storage.get_file_size("file.txt") == 200
        assert self.storage.get_file_size("FILE.txt") == 300
        
        # These should be treated as different files
        assert self.storage.delete_file("File.txt") is True
        assert self.storage.get_file_size("file.txt") == 200
        assert self.storage.get_file_size("FILE.txt") == 300
