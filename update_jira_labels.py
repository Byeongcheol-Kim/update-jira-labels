import re

from jira.client import JIRA
from jira.exceptions import JIRAError
from jira.resources import Issue


class JiraClient:
    def __init__(self, user, password, options):
        self.client = JIRA(basic_auth=(user, password), **options)

    def update_issue_label(self, issue: Issue, label_name: str):
        previous_labels = issue.fields.labels
        updated_labels = previous_labels.append(label_name)
        issue.update(fields={"labels": updated_labels})

    def update_issue_component(self, issue: Issue, coponent_name: str):
        print(issue.fields)

    def find_issue_from_branch_name(self, branch_name: str):
        issue_number = re.search(r"(\w+-\d+)", branch_name).group(1)
        issue: Issue = self.client.issue(id=issue_number)
        return issue
