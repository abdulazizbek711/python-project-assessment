# Python Developer Test Implementation

## Overview
A comprehensive Python implementation featuring data storage, text processing, polygon collision detection, and file system operations.

## Table of Contents
1. Project Structure
2. Requirements
3. Setup
4. Usage
5. Features
6. Logging & Error Handling
7. Testing Guide

## Project Structure
The project follows a simple directory structure with main implementation file and test directories:
```
project/
│
├── main.py          # Main implementation file
├── app.log          # Log file (created automatically)
├── source_dir/      # Test source directory
│   ├── example.txt
│   └── logfile.log
│
└── target_dir/      # Test target directory (created automatically)
```

## Requirements
The project has minimal requirements and runs on standard Python installation:

Python 3.8 or higher is required. No additional packages are needed as the implementation uses only the Python standard library.

## Setup
The setup process involves two main steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create test environment:
   ```bash
   mkdir source_dir
   echo "Line 1\nLine 2\nLine 3\nLine 4\nLine 5" > source_dir/example.txt
   echo "Log 1\nLog 2\nLog 3\nLog 4\nLog 5\nLog 6\nLog 7" > source_dir/logfile.log
   ```

## Usage
To run the application, simply execute the main script. Here's what to expect:

1. Execute the script:
   ```bash
   python main.py
   ```

2. You should see the following output:
   ```python
   {'key1': 'value1', 'key2': 'value2'}
   value1
   [('hello', 3), ('test', 3)]
   True
   [('example.txt', 5), ('logfile.log', 7)]
   ```

## Features

### 1. DataStorage
The DataStorage component provides key-value storage functionality with CRUD operations. It includes:

Methods:
- add(): Add or update key-value pairs
- get(): Retrieve values by key
- delete(): Remove key-value pairs
- list(): Display all stored data

All operations are automatically logged for tracking and debugging purposes.

### 2. Word Frequency Counter
The word frequency analysis component provides text analysis capabilities:

- Performs case-insensitive word counting
- Allows configurable top-k results retrieval
- Returns results in format: [('word', frequency), ...]

### 3. Polygon Collision Detection
The collision detection system handles geometric calculations:

- Takes vertices as (x, y) coordinates
- Works with any polygon shape
- Detects both intersection and containment scenarios

### 4. File Operations
The file processing component manages file system operations:

- Handles directory copying with full content preservation
- Processes multiple file extensions
- Performs line counting for text files

## Logging & Error Handling

### Logging
The application maintains comprehensive logging:

- All logs are stored in app.log
- Uses timestamp format: [YYYY-MM-DD HH:MM:SS] INFO: Operation description
- Covers all operations and error events

### Error Handling
The system includes robust error handling:

- Handles common scenarios like file not found and invalid paths
- Includes processing error management
- Provides comprehensive error logging and appropriate exception handling

## Testing Guide

### Test Scenarios

1. Word Frequency Testing:
   Testing word frequency analysis can be done by modifying input text and trying different k values for result limiting.

2. Polygon Collision Testing:
   Test collision detection by adjusting polygon coordinates and experimenting with different shapes.

3. File Operations Testing:
   Verify file operations by adding various file types and testing different directory structures.

### Important Notes
Before running tests, ensure:

- Paths in main.py are updated for your environment
- Directory permissions are properly set
- app.log is monitored for detailed operation tracking
