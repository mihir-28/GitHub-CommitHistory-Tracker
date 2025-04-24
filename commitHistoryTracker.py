import os
import subprocess
import pandas as pd
from datetime import datetime, timedelta

# Configuration parameters
# ========================
# Base directory containing Git repositories
REPOS_DIR = "path/to/repositories"

# Output file path for the exported commit history
OUTPUT_EXCEL = os.path.join(REPOS_DIR, "commit_history.xlsx")

# List of Git usernames to track (including variations)
YOUR_USERNAMES = ["Your Name", "your-username"]

# Date range for commit history extraction (YYYY-MM-DD format)
START_DATE = "YYYY-MM-DD"  # Start date for commit tracking
END_DATE = "YYYY-MM-DD"  # End date for commit tracking


def get_commit_history(repo_dir, start_date=None, end_date=None):
    """
    Extract commit history for a specific Git repository within a date range.

    Args:
        repo_dir (str): Path to the Git repository
        start_date (str, optional): Start date in YYYY-MM-DD format
        end_date (str, optional): End date in YYYY-MM-DD format

    Returns:
        tuple: (commit_history, all_authors)
            - commit_history: List of lists containing [repo_name, date, message]
            - all_authors: Set of all author names found in the repository
    """
    repo_name = os.path.relpath(repo_dir, REPOS_DIR)
    commit_history = []
    all_authors = set()

    # Validate that the directory is a Git repository
    if not os.path.isdir(os.path.join(repo_dir, ".git")):
        print(f"  Skipping {repo_name} - not a git repository")
        return commit_history, all_authors

    # Retrieve all commit authors from repository history
    all_authors_cmd = ["git", "log", "--format=%an"]
    all_authors_result = subprocess.run(
        all_authors_cmd, cwd=repo_dir, text=True, capture_output=True
    )

    if all_authors_result.returncode == 0:
        all_authors = set(all_authors_result.stdout.splitlines())
        print(f"  All authors in {repo_name}: {', '.join(all_authors)}")

    # Configure git log command with appropriate formatting
    git_cmd = ["git", "log", "--pretty=format:%cd,%an,%s", "--date=iso"]

    # Apply date range filters if specified
    if start_date and end_date:
        git_cmd.append(f"--since={start_date}")
        git_cmd.append(f"--until={end_date}")

    print(f"  Running command: {' '.join(git_cmd)}")
    result = subprocess.run(git_cmd, cwd=repo_dir, text=True, capture_output=True)

    # Process git log output
    if result.returncode == 0:
        lines = result.stdout.splitlines()
        print(f"  Found {len(lines)} total commit entries")

        for line in lines:
            parts = line.split(",", 2)
            if len(parts) == 3:
                date_str, author, message = parts
                # Convert ISO date format to datetime object
                try:
                    date_obj = datetime.fromisoformat(
                        date_str.replace(" ", "T").replace("Z", "+00:00")
                    )
                    # Filter commits by specified usernames
                    if any(
                        username.lower() in author.lower()
                        for username in YOUR_USERNAMES
                    ):
                        commit_history.append([repo_name, date_obj, message])
                except ValueError:
                    # Skip entries with invalid date format
                    continue

        print(f"  Found {len(commit_history)} commits matching your username(s)")
    else:
        print(f"  Error running git log: {result.stderr}")

    return commit_history, all_authors


def find_git_repos(base_dir):
    """
    Recursively find all Git repositories within a base directory.

    Args:
        base_dir (str): Base directory to search for Git repositories

    Returns:
        list: Paths to all discovered Git repositories
    """
    git_repos = []

    # Traverse directory tree
    for root, dirs, files in os.walk(base_dir):
        # Avoid processing output directory if it exists
        if os.path.basename(root) == os.path.basename(OUTPUT_EXCEL).split(".")[0]:
            continue

        # Identify Git repositories
        if ".git" in dirs or os.path.isdir(os.path.join(root, ".git")):
            git_repos.append(root)
            # Optimize traversal by skipping .git directories
            if ".git" in dirs:
                dirs.remove(".git")

    return git_repos


def collect_all_commits():
    """
    Main function to collect and process commit history across all repositories.

    Searches for Git repositories, extracts commit information for specified users,
    and exports the results to an Excel file.
    """
    all_commits = []
    all_unique_authors = set()

    print(f"Collecting commits from {START_DATE} to {END_DATE}")
    print(f"Looking for commits by usernames: {', '.join(YOUR_USERNAMES)}")

    # Discover Git repositories
    git_repos = find_git_repos(REPOS_DIR)
    print(f"Found {len(git_repos)} Git repositories")

    # Process each repository
    for repo_path in git_repos:
        repo_name = os.path.relpath(repo_path, REPOS_DIR)
        print(f"Processing repository: {repo_name}")
        commits, authors = get_commit_history(repo_path, START_DATE, END_DATE)
        all_commits.extend(commits)
        all_unique_authors.update(authors)

    # Report results summary
    print("\n=== Summary ===")
    print(
        f"All unique authors found across repositories: {', '.join(all_unique_authors)}"
    )
    print(f"Your configured usernames: {', '.join(YOUR_USERNAMES)}")

    # Export results if commits were found
    if all_commits:
        df = pd.DataFrame(all_commits, columns=["Repository", "Date", "Commit Message"])

        # Sort chronologically (newest first)
        df = df.sort_values(by="Date", ascending=False)

        # Format dates for readability
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Export to Excel
        df.to_excel(OUTPUT_EXCEL, index=False)
        print(f"Commit history has been exported to {OUTPUT_EXCEL}")
        print(f"Total commits found: {len(df)}")
    else:
        print("No commits found for your username.")
        print("Please check if your username(s) match any of the authors listed above.")


if __name__ == "__main__":
    collect_all_commits()
