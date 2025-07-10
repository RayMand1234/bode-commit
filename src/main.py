import sys
from urllib.parse import urlparse
from datetime import datetime

import dotenv
import urllib3
import gitlab

from validations import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '/.env'), override=True)


def connect_to_gitlab(gitlab_url, git_token):
    myLogger.logger.info(f'Connecting to GitLab at {gitlab_url}')
    gl = gitlab.Gitlab(gitlab_url, private_token=git_token, ssl_verify=False)
    gl.auth()
    return gl


def is_valid_gitlab_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc, parsed.path])
    except:
        return False


def get_fallback_branch(project):
    """
    Returns the most recently updated non-default branch to use as a fallback.
    If no fallback branch is found, returns None.
    
    Args:
        project: A GitLab project object (already fetched via python-gitlab)
    
    Returns:
        The name of the fallback branch (str) or None
    """
    default_branch = project.default_branch

    # Get all branches except the default
    branches = project.branches.list(all=True)
    candidate_branches = [b for b in branches if b.name != default_branch]

    if not candidate_branches:
        return None

    # Sort by commit date descending
    def parse_commit_date(branch):
        commit_info = branch.commit
        return datetime.strptime(commit_info['committed_date'], "%Y-%m-%dT%H:%M:%S.%f%z")

    sorted_branches = sorted(candidate_branches, key=parse_commit_date, reverse=True)

    return sorted_branches[0].name


def validate_repository(gitlab_url, gitlab_token, min_commits, max_commits):
    """
    Validate a GitLab repository and return validation results.
    
    Args:
        gitlab_url (str): Full GitLab project URL
        gitlab_token (str): GitLab authentication token
        
    Returns:
        dict: Dictionary containing validation results
    """
    if not is_valid_gitlab_url(gitlab_url):
        raise ValueError("Invalid GitLab URL format")

    parsed_url = urlparse(gitlab_url)
    gl = connect_to_gitlab(parsed_url.scheme + "://" + parsed_url.netloc, gitlab_token)
    project = gl.projects.get(parsed_url.path[1:])
    latest_version = validate_main_latest_version(project)

    if not latest_version:
        myLogger.logger.warning("OUTDATED MAIN BRANCH - FALLBACK TO CHILD BRANCH")
        ref_branch = get_fallback_branch(project)
    else:
        ref_branch = 'main'

    commits = project.commits.list(ref_name=ref_branch, all=True)

    myLogger.logger.info("Starting validation process")
    enough_commits = validate_commits_range(commits, min_commits, max_commits)
    significant_commits = validate_significant_commits(commits)
    commits_standard_status = validate_commits_standard(commits)
    gitignore_status = validate_gitignore(project, ref_branch)
    succint_commits = validate_succinct_commits(commits)

    return {
        'commit_volume': enough_commits,
        'significant_commits': significant_commits['validationStatus'],
        'commit_standards': commits_standard_status['validationStatus'],
        'has_gitignore': gitignore_status,
        'succint_commits': succint_commits,
        'latest_version': latest_version
    }


if __name__ == "__main__":

    if len(sys.argv) < 1:
        myLogger.logger.error(
            "Failed to pass arguments. Check the inputs. If the bug persists, communicate with the creater - Ray Mandelevi 9369350")
    else:
        gitlab_token = os.getenv('GITLAB_TOKEN')
        project_url = sys.argv[1]
        min_commits = int(sys.argv[2])
        max_commits = int(sys.argv[3])

        results = validate_repository(project_url, gitlab_token, min_commits, max_commits)

        print('------------------------------------------')
        print('Satisfying Commit Volume: ' + ('passed' if results['commit_volume'] else 'failed'))
        print('Significant Commits: ' + results['significant_commits'])
        print('Commits Meet Standard: ' + results['commit_standards'])
        print('Contains Valid .gitignore: ' + ('passed' if results['has_gitignore'] else 'failed'))
        print('Succint Commits: ' + ('passed' if results['succint_commits'] else 'failed'))
        print('Latest Version On Main: ' + ('passed' if results['latest_version'] else 'failed'))
        print('------------------------------------------')
