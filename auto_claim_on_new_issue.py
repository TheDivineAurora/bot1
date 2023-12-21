import os
import json
import requests
import time

owner = "opencodeiiita"


repositories = ["Collaborative-Web-2023","Scoop-Frontend", "GrepIt-Backend", "Hitch-Backend","GrepIt-Frontend","Code-Digger-2023","Hitch-Frontend","Scoop-Backend",]  # Replace with your repository names


github_token = "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"  # Replace with your actual GitHub personal access token


def get_issues(repo):
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues", headers=headers)
    return response.json()

def comment_on_issue(repo, issue_number):
    comment = "claim"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
        json={"body": comment},
        headers=headers,
    )
    return response.status_code

def main():
    try:
        # Initialize the previous_issues dictionary with the initial existing issues (excluding pull requests) for each repository
        previous_issues = {}
        for repo in repositories:
            issues = get_issues(repo)
            issue_numbers = [issue["number"] for issue in issues if "pull_request" not in issue]
            previous_issues[repo] = set(issue_numbers)

        print("Initial previous_issues:", previous_issues)

        while True:
            for repo in repositories:
                issues = get_issues(repo)
                current_issues = set(issue["number"] for issue in issues if "pull_request" not in issue)

                new_issues = current_issues - previous_issues[repo]

                if len(new_issues) > 0:
                    for issue_number in new_issues:
                        status_code = comment_on_issue(repo, issue_number)

                        if status_code == 201:
                            print(f"Successfully commented 'claim' on issue {issue_number} in {owner}/{repo}.")
                        else:
                            print(f"Failed to comment 'claim' on issue {issue_number} in {owner}/{repo}. Status code: {status_code}")

                previous_issues[repo] = current_issues

            time.sleep(20)  # Sleep for 5 seconds before checking again
    except KeyboardInterrupt:
        print("Script terminated.")

if __name__ == "__main__":
    main()