from dataclasses import dataclass


@dataclass
class JiraComponent:
    name: str


@dataclass
class InwardIssue:
    key: str


@dataclass
class JiraIssueLinkType:
    name: str
    inward: str


@dataclass
class JiraIssueLink:
    inwardIssue: InwardIssue
    type: JiraIssueLinkType
