"""
Shared Cloud File Storage Implementation

This file contains the skeleton for implementing a shared cloud file storage system with 4 levels of complexity.
Complete the implementation of the FileStorage class to pass all tests.

Level 1: Basic file operations (add, delete, query)
Level 2: File permissions and access control
Level 3: Directory structure support  
Level 4: File versioning and history

Example usage:
    storage = FileStorage()
    
    # Level 1 examples:
    storage.add_file("document.txt", 1024)  # Returns True
    storage.add_file("document.txt", 512)   # Returns False (duplicate)
    storage.get_file_size("document.txt")   # Returns 1024
    storage.delete_file("document.txt")     # Returns True
    storage.get_file_size("document.txt")   # Returns None
    
    # Level 2 examples:
    storage.add_file("large.txt", 2048)
    storage.add_file("medium.txt", 1024)
    storage.add_file("small.txt", 512)
    storage.get_largest_n(2)  # Returns ["large.txt(2048)", "medium.txt(1024)"]
    storage.get_largest_n(5)   # Returns all files sorted by size
    
    # Level 3 examples:
    storage.add_user("alice", 5000)  # Alice gets 5000 bytes
    storage.add_user("bob", 3000)    # Bob gets 3000 bytes
    storage.add_file_by("alice", "doc.txt", 1000)  # Returns 4000 (remaining)
    storage.add_file_by("bob", "image.jpg", 2000)  # Returns 1000 (remaining)
    storage.merge_users("alice", "bob")  # Alice gets Bob's files and storage
    
    # Level 4 examples:
    storage.add_user("alice", 5000)
    storage.add_file_by("alice", "doc1.txt", 1000)
    storage.add_file_by("alice", "doc2.txt", 2000)
    backup_count = storage.backup("alice")  # Returns 2 (files backed up)
    storage.add_file_by("alice", "doc3.txt", 1500)  # Add more files
    restore_count = storage.restore("alice")  # Returns 2 (files restored, doc3.txt removed)

Your implementation should pass all tests in test/test_level1.py, test/test_level2.py, test/test_level3.py, and test/test_level4.py
"""

from typing import Optional


class FileStorage:
    """
    A shared cloud file storage system that stores file metadata in memory.
    
    The system maintains a mapping of filename to file metadata and provides methods
    to add, delete, and query files with increasing levels of complexity.
    """
    
    def __init__(self):
        """Initialize the file storage with an empty file system."""
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 1 METHODS
    # ============================================================================
    
    def add_file(self, name: str, size: int) -> bool:
        """
        Add a file to the storage system.
        
        Args:
            name: The filename
            size: The size of the file in bytes
            
        Returns:
            False if the filename already exists, True if successfully added
        """
        # TODO: Implement this method
        pass
    
    def delete_file(self, name: str) -> bool:
        """
        Delete a file from the storage system.
        
        Args:
            name: The filename to delete
            
        Returns:
            False if the file does not exist, True if successfully deleted
        """
        # TODO: Implement this method
        pass
    
    def get_file_size(self, name: str) -> Optional[int]:
        """
        Get the size of a file.
        
        Args:
            name: The filename to query
            
        Returns:
            None if the file does not exist, otherwise the size of the file
        """
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 2 METHODS
    # ============================================================================
    
    def get_largest_n(self, n: int) -> list[str]:
        """
        Get the n largest files by size.
        
        Args:
            n: The number of largest files to return
            
        Returns:
            List of formatted strings in format ['filename1(size1)', 'filename2(size2)', ...]
            Files are sorted by size (largest first), with alphabetical sorting for ties
            Returns empty list if no files exist or n <= 0
        """
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 3 METHODS
    # ============================================================================
    
    def add_user(self, user_id: str, capacity: int) -> bool:
        """
        Add a user to the file storage system.
        
        Args:
            user_id: Unique identifier for the user
            capacity: Storage allowance in bytes for the user
            
        Returns:
            False if the user already exists, True if successfully added
        """
        # TODO: Implement this method
        pass
    
    def add_file_by(self, user_id: str, name: str, size: int) -> Optional[int]:
        """
        Add a file to the storage system by a specific user.
        
        Args:
            user_id: The user adding the file
            name: The filename
            size: The size of the file in bytes
            
        Returns:
            None if user doesn't exist, file already exists, or would exceed capacity
            Otherwise returns the remaining storage allowance for the user
        """
        # TODO: Implement this method
        pass
    
    def merge_users(self, user_id_1: str, user_id_2: str) -> bool:
        """
        Merge two users by reassigning all of user2's files to user1.
        
        Args:
            user_id_1: The user to receive all files and storage
            user_id_2: The user to be deleted after merging
            
        Returns:
            False if user_id_1 == user_id_2 or either user doesn't exist
            True if merge operation succeeds
        """
        # TODO: Implement this method
        pass
    
    # ============================================================================
    # LEVEL 4 METHODS
    # ============================================================================
    
    def backup(self, user_id: str) -> Optional[int]:
        """
        Create a backup of the user's files at the current point in time.
        
        Args:
            user_id: The user to create backup for
            
        Returns:
            Number of files backed up, None if user doesn't exist
            At most one backup per user - subsequent backups overwrite previous ones
        """
        # TODO: Implement this method
        pass
    
    def restore(self, user_id: str) -> Optional[int]:
        """
        Restore the user's files from their backup.
        
        Args:
            user_id: The user to restore files for
            
        Returns:
            Number of files successfully restored, None if user doesn't exist
            If file exists and is owned by different user, it cannot be restored
            If backup is empty or doesn't exist, all user's files are deleted
            Restore removes any present files not in the backup
        """
        # TODO: Implement this method
        pass
