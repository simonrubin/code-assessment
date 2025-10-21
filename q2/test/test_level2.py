"""
Question 2 - Level 2 Tests: File Size Querying

Test cases for the get_largest_n function:
- get_largest_n: Returns n largest files by size with alphabetical tie-breaking

These tests validate functionality without being implementation-specific.
"""

import pytest
from impl import FileStorage


class TestQuestion2Level2:
    """Test cases for Question 2 Level 2 - File Size Querying."""
    
    def setup_method(self):
        """Set up a fresh FileStorage instance for each test."""
        self.storage = FileStorage()
    
    def test_get_largest_n_empty_storage(self):
        """Test get_largest_n with empty storage."""
        result = self.storage.get_largest_n(5)
        assert result == []
    
    def test_get_largest_n_zero_or_negative(self):
        """Test get_largest_n with zero or negative n."""
        self.storage.add_file("test.txt", 100)
        
        assert self.storage.get_largest_n(0) == []
        assert self.storage.get_largest_n(-1) == []
        assert self.storage.get_largest_n(-5) == []
    
    def test_get_largest_n_single_file(self):
        """Test get_largest_n with single file."""
        self.storage.add_file("single.txt", 1024)
        
        result = self.storage.get_largest_n(1)
        assert result == ["single.txt(1024)"]
        
        result = self.storage.get_largest_n(5)
        assert result == ["single.txt(1024)"]
    
    def test_get_largest_n_multiple_files_different_sizes(self):
        """Test get_largest_n with files of different sizes."""
        files = [
            ("small.txt", 100),
            ("medium.txt", 1000),
            ("large.txt", 5000),
            ("tiny.txt", 50)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        # Test getting top 2
        result = self.storage.get_largest_n(2)
        assert result == ["large.txt(5000)", "medium.txt(1000)"]
        
        # Test getting top 3
        result = self.storage.get_largest_n(3)
        assert result == ["large.txt(5000)", "medium.txt(1000)", "small.txt(100)"]
        
        # Test getting all files
        result = self.storage.get_largest_n(4)
        assert result == ["large.txt(5000)", "medium.txt(1000)", "small.txt(100)", "tiny.txt(50)"]
    
    def test_get_largest_n_with_ties_alphabetical_sort(self):
        """Test get_largest_n with files of same size (alphabetical tie-breaking)."""
        files = [
            ("zebra.txt", 1000),
            ("apple.txt", 1000),
            ("banana.txt", 1000),
            ("cherry.txt", 2000)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        # Test getting top 3 (should include all 1000-byte files alphabetically)
        result = self.storage.get_largest_n(3)
        assert result == ["cherry.txt(2000)", "apple.txt(1000)", "banana.txt(1000)"]
        
        # Test getting all files
        result = self.storage.get_largest_n(4)
        assert result == ["cherry.txt(2000)", "apple.txt(1000)", "banana.txt(1000)", "zebra.txt(1000)"]
    
    def test_get_largest_n_more_than_available(self):
        """Test get_largest_n when requesting more files than available."""
        self.storage.add_file("file1.txt", 100)
        self.storage.add_file("file2.txt", 200)
        
        # Request more files than available
        result = self.storage.get_largest_n(5)
        assert result == ["file2.txt(200)", "file1.txt(100)"]
    
    def test_get_largest_n_exactly_available(self):
        """Test get_largest_n when requesting exactly the number of available files."""
        files = [
            ("a.txt", 100),
            ("b.txt", 200),
            ("c.txt", 300)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        result = self.storage.get_largest_n(3)
        assert result == ["c.txt(300)", "b.txt(200)", "a.txt(100)"]
    
    def test_get_largest_n_mixed_sizes_and_ties(self):
        """Test get_largest_n with complex size patterns and ties."""
        files = [
            ("file_a.txt", 1000),
            ("file_b.txt", 1000),
            ("file_c.txt", 500),
            ("file_d.txt", 2000),
            ("file_e.txt", 1000),
            ("file_f.txt", 500)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        # Test getting top 4
        result = self.storage.get_largest_n(4)
        expected = [
            "file_d.txt(2000)",
            "file_a.txt(1000)",
            "file_b.txt(1000)",
            "file_e.txt(1000)"
        ]
        assert result == expected
    
    def test_get_largest_n_zero_sizes(self):
        """Test get_largest_n with files of zero size."""
        files = [
            ("zero1.txt", 0),
            ("zero2.txt", 0),
            ("normal.txt", 100)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        result = self.storage.get_largest_n(3)
        assert result == ["normal.txt(100)", "zero1.txt(0)", "zero2.txt(0)"]
    
    def test_get_largest_n_negative_sizes(self):
        """Test get_largest_n with files of negative sizes."""
        files = [
            ("negative.txt", -100),
            ("positive.txt", 100),
            ("zero.txt", 0)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        result = self.storage.get_largest_n(3)
        assert result == ["positive.txt(100)", "zero.txt(0)", "negative.txt(-100)"]
    
    def test_get_largest_n_special_characters_in_names(self):
        """Test get_largest_n with special characters in filenames."""
        files = [
            ("file with spaces.txt", 1000),
            ("file-with-dashes.txt", 1000),
            ("file_with_underscores.txt", 1000),
            ("file.with.dots.txt", 2000)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        result = self.storage.get_largest_n(4)
        expected = [
            "file.with.dots.txt(2000)",
            "file with spaces.txt(1000)",
            "file-with-dashes.txt(1000)",
            "file_with_underscores.txt(1000)"
        ]
        assert result == expected
    
    def test_get_largest_n_case_sensitive_sorting(self):
        """Test that get_largest_n handles case-sensitive alphabetical sorting."""
        files = [
            ("Apple.txt", 1000),
            ("apple.txt", 1000),
            ("BANANA.txt", 1000),
            ("banana.txt", 1000)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        result = self.storage.get_largest_n(4)
        expected = [
            "Apple.txt(1000)",
            "BANANA.txt(1000)",
            "apple.txt(1000)",
            "banana.txt(1000)"
        ]
        assert result == expected
    
    def test_get_largest_n_after_file_deletion(self):
        """Test get_largest_n after files have been deleted."""
        files = [
            ("file1.txt", 100),
            ("file2.txt", 200),
            ("file3.txt", 300),
            ("file4.txt", 400)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        # Delete some files
        self.storage.delete_file("file2.txt")
        self.storage.delete_file("file4.txt")
        
        result = self.storage.get_largest_n(5)
        assert result == ["file3.txt(300)", "file1.txt(100)"]
    
    def test_get_largest_n_format_consistency(self):
        """Test that get_largest_n returns consistent formatting."""
        files = [
            ("simple.txt", 123),
            ("file with spaces.txt", 456),
            ("file-with-dashes.txt", 789),
            ("file_with_underscores.txt", 101112)
        ]
        
        for name, size in files:
            self.storage.add_file(name, size)
        
        result = self.storage.get_largest_n(4)
        
        # Verify format: each item should be "filename(size)"
        for item in result:
            assert "(" in item and ")" in item
            assert item.count("(") == 1 and item.count(")") == 1
            assert item.endswith(")")
            
            # Extract filename and size
            filename = item[:item.rfind("(")]
            size_str = item[item.rfind("(")+1:item.rfind(")")]
            
            # Verify size is numeric
            assert size_str.isdigit() or (size_str.startswith("-") and size_str[1:].isdigit())
