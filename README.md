# Coding Quiz Collection

A collection of progressive coding challenges, each with 4 levels of increasing complexity.

## Repository Structure

```
coding-quiz/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── q1/                # Question 1: In-Memory Database
│   ├── README.md      # Question 1 requirements
│   ├── impl.py        # Your implementation
│   ├── solution.py    # Complete solution (reference)
│   └── test/          # Test files for all 4 levels
└── q2/                # Question 2: Shared Cloud File Storage
    ├── README.md      # Question 2 requirements
    ├── impl.py        # Your implementation
    ├── solution.py    # Complete solution (reference)
    └── test/          # Test files for all 4 levels
```

## Questions

### Question 1: In-Memory Database
**Status**: ✅ Complete  
**Levels**: 4  
**Focus**: Data structures, CRUD operations, timestamp-based operations, TTL, backup/restore

Implement an in-memory database with progressive features:
- **Level 1**: Basic CRUD operations
- **Level 2**: Scanning and prefix filtering  
- **Level 3**: Timestamp-based operations with TTL
- **Level 4**: Backup and restore with TTL adjustment

[View Question 1 Details →](q1/README.md)

### Question 2: Shared Cloud File Storage
**Status**: ✅ Complete  
**Levels**: 4  
**Focus**: File management, user systems, capacity limits, backup/restore

Implement a shared cloud file storage system with progressive features:
- **Level 1**: Basic file operations (add, delete, query)
- **Level 2**: File size querying with sorting
- **Level 3**: User management with capacity limits
- **Level 4**: Backup and restore functionality

[View Question 2 Details →](q2/README.md)

## Getting Started

1. **Choose a question**: Navigate to the question directory (e.g., `q1/` or `q2/`)
2. **Read the requirements**: Check the question's README for detailed specifications
3. **Implement your solution**: Edit the `impl.py` file in the question directory
4. **Test your implementation**: Run the tests to verify your solution

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Navigate to a question**:
   ```bash
   cd q1  # In-Memory Database
   cd q2  # Shared Cloud File Storage
   ```

3. **Run tests**:
   ```bash
   # Test specific level
   python -m pytest test/test_level1.py -v
   
   # Test all levels
   python -m pytest test/ -v
   ```

## Testing

Each question includes comprehensive test suites:
- **Level 1**: Basic functionality tests
- **Level 2**: Extended feature tests  
- **Level 3**: Advanced feature tests
- **Level 4**: Complex scenario tests

Tests cover:
- ✅ Happy path scenarios
- ✅ Edge cases and error conditions
- ✅ Performance considerations
- ✅ Integration between levels

## Contributing

This repository is designed for educational purposes. Each question:
- Has a clear progression from simple to complex
- Includes comprehensive test coverage
- Provides detailed documentation
- Offers a complete reference solution

## Questions Structure

Each question follows this pattern:
- **4 levels** of increasing complexity
- **Progressive features** that build upon previous levels
- **Comprehensive tests** for each level
- **Clear documentation** with examples
- **Reference solution** for verification

## Available Questions

Currently implemented questions:
- **q1**: In-Memory Database (✅ Complete)
- **q2**: Shared Cloud File Storage (✅ Complete)

## Future Questions

Additional questions will be added following the same structure:
- `q3/` - [Future question]
- `q4/` - [Future question]
- etc.

Each new question will introduce different problem domains and algorithmic challenges while maintaining the consistent 4-level progression structure.