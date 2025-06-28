# ReviewCommits

A Python script that analyzes GitLab repositories to validate commit quality and repository standards. This tool helps ensure that your repository follows best practices for commit messages, commit volume, and repository structure.

Created by Ray Mandelevi

## Features

- Validates commit message standards (Conventional Commits)
- Checks commit volume against specified thresholds
- Analyzes commit significance using AI
- Verifies .gitignore implementation
- Ensures commits are concise and meaningful
- Checks if the main branch is up to date

## Prerequisites

- Python 3.6 or higher
- GitLab account with API access
- Groq API key for AI-powered commit analysis

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ReviewCommits.git
cd ReviewCommits
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

You don't need to create any environment variables.</br>
In fact the script does it for you to save your credentials such as:
   - gitlab token
   - groq api key

To grant you efficient setup each boot!

## Usage

1. Run the script:

```bash
python src/main.py
```

2. When prompted:
   - Enter the full GitLab project URL (e.g., https://gitlab.com/group/project)
   - Specify the minimum number of commits
   - Specify the maximum number of commits

## Output

The script will provide a validation report with the following checks:

- ✅ Commit Volume: Verifies if the number of commits falls within the specified range
- ✅ Significant Commits: AI-powered analysis of commit message quality
- ✅ Commit Standards: Checks if commits follow Conventional Commits format
- ✅ .gitignore: Verifies proper .gitignore implementation
- ✅ Succinct Commits: Ensures commit messages are concise
- ✅ Latest Version: Checks if the main branch is up to date

## Validation Rules

### Commit Standards

- Follows Conventional Commits format (e.g., `feat(scope): description`)
- Accepts common phrases like "Initial commit" or "Merge branch"
- Requires meaningful commit messages

### Commit Volume

- Configurable minimum and maximum number of commits
- Excludes fix, hotfix, docs, merge, and initial commit messages from count

### Significant Commits

- AI-powered analysis of commit message quality
- Ensures messages provide basic context and purpose
- Rejects unhelpful messages like "stuff" or "more fixes"

### Succinct Commits

- Maximum 60 characters for commit descriptions
- Allows up to 25% of commits to exceed the character limit

## Dependencies

- python-gitlab: GitLab API client
- python-dotenv: Environment variable management
- openai: Groq API client for AI analysis
- pathspec: .gitignore pattern matching
- urllib3: HTTP client

## Contributing

Feel free to submit issues and enhancement requests!
