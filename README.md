# GitHub Commit History Tracker

A comprehensive Python utility for extracting, analyzing, and reporting Git commit history across multiple repositories, designed to help developers track their contributions over time.

## Overview

This tool recursively scans a directory structure containing multiple Git repositories and extracts detailed commit history information for specified users within a defined date range. The results are consolidated into a single Excel spreadsheet for easy review, analysis, and reporting. Perfect for developers who need to track their work across multiple projects or for team leads who want to monitor contribution patterns.

## Features

- **Recursive Repository Scanning**: Automatically discovers Git repositories in nested directory structures
- **Multiple Username Support**: Tracks commits from different username variations (full name, username, email)
- **Flexible Date Filtering**: Limits results to specific time periods with precise date range control
- **Author Identification**: Provides visibility into all contributors across scanned repositories
- **Smart Filtering**: Includes case-insensitive username matching for more accurate results
- **Excel Export**: Generates a professional, well-formatted Excel spreadsheet for further analysis
- **Chronological Organization**: Sorts commits by date (oldest first or newest first)
- **Comprehensive Logging**: Provides detailed progress information during execution
- **Repository Structure Preservation**: Maintains original directory structure in reports for better context
- **Error Handling**: Gracefully handles missing repositories, permission issues, and invalid date formats

## Requirements

- **Python 3.6+**: Takes advantage of modern Python features for efficient execution
- **pandas library**: Used for data manipulation and organization (v1.0.0 or higher recommended)
- **openpyxl library**: Required for Excel file generation and formatting (v3.0.0 or higher)
- **Git**: Command-line Git installation accessible from the execution environment
- **Sufficient Permissions**: Read access to all repository directories and write access for output file

## Installation

1. Clone this repository or download the script file to your local environment
2. Install required dependencies using pip:

```bash
pip install pandas openpyxl
```

3. Ensure Git is installed and properly configured on your system

## Configuration

Edit the following variables at the top of the script to configure for your specific environment:

```python
# Base directory containing Git repositories
REPOS_DIR = "path/to/repositories"  # Path to your repositories directory

# Output file path for the exported commit history
OUTPUT_EXCEL = os.path.join(REPOS_DIR, "commit_history.xlsx")

# List of Git usernames to track (including variations)
YOUR_USERNAMES = ["Your Name", "your-username"]  # Add all variations of your username

# Date range for commit history extraction (YYYY-MM-DD format)
START_DATE = "YYYY-MM-DD"  # Start date for commit tracking
END_DATE = "YYYY-MM-DD"    # End date for commit tracking
```

## Usage

### Basic Execution

Run the script from the command line:

```bash
python CommitHistoryTracker.py
```

### Process Flow

1. **Initialization**: Script reads configuration settings and prepares scanning environment
2. **Repository Discovery**: Recursively searches through the specified base directory for Git repositories
3. **Repository Processing**: For each repository found:
   - Validates Git repository structure
   - Retrieves list of all commit authors
   - Extracts commit history using optimized Git commands
   - Filters commits by author and date range
   - Collects matching commits with repository, date, and message details
4. **Data Consolidation**: Combines commit information from all repositories
5. **Sorting and Formatting**: Organizes commits chronologically and formats dates
6. **Excel Generation**: Creates a formatted Excel document with the consolidated data
7. **Summary Output**: Provides statistics on repositories scanned and commits found

### Output Format

The generated Excel file includes the following columns:

- **Repository**: Path to repository relative to base directory
- **Date**: Commit timestamp in YYYY-MM-DD HH:MM:SS format
- **Commit Message**: Full commit message

## Advanced Customization

### Modifying Git Command Parameters

You can customize the Git log command format by editing the `git_cmd` variable in the `get_commit_history` function:

```python
git_cmd = ["git", "log", "--pretty=format:%cd,%an,%s", "--date=iso"]
```

### Adding Additional Fields

To include more information about each commit (like commit hash or changed files), modify both the Git log command and the data collection logic:

```python
# Example to include commit hash
git_cmd = ["git", "log", "--pretty=format:%H,%cd,%an,%s", "--date=iso"]

# Then update the processing logic to include the hash in the commit data
hash_id, date_str, author, message = parts
commit_history.append([repo_name, hash_id, date_obj, message])
```

### Sorting Options

To change the sort order of commits in the output:

```python
# Newest first (most recent commits at top)
df = df.sort_values(by="Date", ascending=False)

# Oldest first (historical order)
df = df.sort_values(by="Date", ascending=True)
```

## Troubleshooting

### No Repositories Found

- Verify the `REPOS_DIR` path is correct and accessible
- Ensure repositories contain proper `.git` directories
- Check file system permissions for the directory tree

### No Commits Found

- Compare the output authors list with your configured usernames
- Try adding username variations (with different capitalization, email addresses)
- Adjust the date range to ensure it encompasses your activity period
- Check that the repositories have commits matching your criteria

### Excel Output Issues

- Ensure the `openpyxl` package is correctly installed
- Verify you have write permissions for the output file location
- Close any open instances of the Excel file before running the script

### Performance Considerations

For very large repository collections:
- Consider processing repositories in batches
- Add repository exclusion patterns for directories that shouldn't be scanned
- Filter commits by specific files or paths to reduce processing time

## Future Enhancements

- Command-line arguments for configuration options
- HTML report generation with interactive filtering
- Graphical commit history visualization
- Team contribution analysis and comparison
- Integration with project management systems
- Branch-specific commit history analysis

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) for details.

## Acknowledgments

- Developed using insights from Git's commit tracking capabilities
- Inspired by the need for cross-repository contribution visibility
- Built with Python's powerful data processing ecosystem
