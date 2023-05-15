import dataclasses
import re
from dataclasses import asdict
from typing import Dict, List

from jira.client import JIRA
from jira.resources import Issue

from apps.dto import JiraComponent, JiraIssueLink, InwardIssue, JiraIssueLinkType


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d  # Not a dataclass field


class JiraClient:
    def __init__(self, user, password, options):
        self.client = JIRA(basic_auth=(user, password), **options)

    def get_ticket(self, issue_number: str):
        return self.client.issue(id=issue_number)

    def find_issue_from_branch_name(self, branch_name: str):
        issue_number = re.search(r"(\w+-\d+)", branch_name).group(1)
        issue: Issue = self.client.issue(id=issue_number)
        return issue

    def get_linked_issues(self, issue: Issue) -> List[Dict[str, str]]:
        result = []

        for issuelink in issue.raw["fields"]["issuelinks"]:
            result.append(
                asdict(
                    JiraIssueLink(
                        inwardIssue=InwardIssue(key=issuelink["inwardIssue"]["key"] if "inwardIssue" in issuelink else issuelink["outwardIssue"]["key"]),
                        type=JiraIssueLinkType(
                            name=issuelink["type"]["name"],
                            inward=issuelink["type"]["inward"],
                        ),
                    )
                )
            )
        return result

    def append_issue_label(self, issue: Issue, label_name: str):
        issue.update(update={"labels": [{"add": label_name}]})

    def remove_issue_label(self, issue: Issue, label_name: str):
        issue.update(update={"labels": [{"remove": label_name}]})

    def append_issue_component(self, issue: Issue, component: str):
        issue.update(update={"components": [{"add": {"name": component}}]})

    def remove_issue_component(self, issue: Issue, component: str):
        issue.update(update={"components": [{"remove": {"name": component}}]})
