from unittest import mock

import pytest
from dotenv import dotenv_values

from apps.dto import JiraComponent
from apps.jira_clients import (
    JiraClient,
)


class TestJiraClient:
    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.env = dotenv_values("../.env")
        self.test_ticket_number = self.env.get("TEST_TICKET_NUMBER")
        self.user = self.env.get("JIRA_USER")
        self.password = self.env.get("JIRA_PASSWORD")
        self.options = {"server": self.env.get("JIRA_SERVER")}
        self.jira_client = JiraClient(self.user, self.password, self.options)

        self.orderyo_component = self.jira_client.client.component(id=19854)
        self.test_component = self.jira_client.client.component(id=20091)

    def test_get_issue(self):
        issue = self.jira_client.get_ticket(self.test_ticket_number)

        # TEST labels
        assert issue.get_field("labels") == ["msa"]

        # TEST components
        components = issue.get_field("components")
        ordery_component = self.jira_client.client.component(id=19854)
        assert ordery_component.name == "orderyo"
        assert components == [ordery_component]
        assert issue.raw["fields"]["issuelinks"] == [
            {
                "id": "258959",
                "inwardIssue": {
                    "fields": mock.ANY,
                    "id": "188326",
                    "key": "ORDER-4135",
                    "self": "https://rgpkorea.atlassian.net/rest/api/2/issue/188326",
                },
                "self": "https://rgpkorea.atlassian.net/rest/api/2/issueLink/258959",
                "type": {
                    "id": "10001",
                    "inward": "is cloned by",
                    "name": "Cloners",
                    "outward": "clones",
                    "self": "https://rgpkorea.atlassian.net/rest/api/2/issueLinkType/10001",
                },
            },
            {
                "id": "258960",
                "inwardIssue": {
                    "fields": mock.ANY,
                    "id": "188327",
                    "key": "ORDER-4136",
                    "self": "https://rgpkorea.atlassian.net/rest/api/2/issue/188327",
                },
                "self": "https://rgpkorea.atlassian.net/rest/api/2/issueLink/258960",
                "type": {
                    "id": "10001",
                    "inward": "is cloned by",
                    "name": "Cloners",
                    "outward": "clones",
                    "self": "https://rgpkorea.atlassian.net/rest/api/2/issueLinkType/10001",
                },
            },
        ]

    def test_get_linked_issues(self):
        issue = self.jira_client.get_ticket(self.test_ticket_number)

        linked_issues = self.jira_client.get_linked_issues(issue)
        assert linked_issues == [
            {
                "inwardIssue": {"key": "ORDER-4135"},
                "type": {"inward": "is cloned by", "name": "Cloners"},
            },
            {
                "inwardIssue": {"key": "ORDER-4136"},
                "type": {"inward": "is cloned by", "name": "Cloners"},
            },
        ]

    def test_find_issue_from_branch_name(self):
        branch_name = "order-3867-get-order-info-from-orderyo-when-write-review2"
        issue = self.jira_client.find_issue_from_branch_name(branch_name)
        assert issue.key == "ORDER-3867"


    def test_append_issue_label_and_remove_label(self):
        # TEST append_issue_label
        issue = self.jira_client.get_ticket(self.test_ticket_number)
        self.jira_client.append_issue_label(issue, "test")
        assert issue.get_field("labels") == ["msa", "test"]

        self.jira_client.remove_issue_label(issue, "test")
        assert issue.get_field("labels") == ["msa"]

    def test_remove_label_when_value_error(self):
        issue = self.jira_client.get_ticket(self.test_ticket_number)
        self.jira_client.remove_issue_label(issue, "test")
        assert issue.get_field("labels") == ["msa"]

    def test_append_duplicate_labels(self):
        issue = self.jira_client.get_ticket(self.test_ticket_number)
        self.jira_client.append_issue_label(issue, "test")
        assert issue.get_field("labels") == ["msa", "test"]
        self.jira_client.append_issue_label(issue, "test")
        assert issue.get_field("labels") == ["msa", "test"]

    def test_append_issue_component_and_remove_component(self):
        # TEST append_issue_label
        issue = self.jira_client.get_ticket(self.test_ticket_number)
        self.jira_client.append_issue_component(issue, JiraComponent(name="bau"))
        assert issue.get_field("components") == [
            self.test_component,
            self.orderyo_component,
        ]

        self.jira_client.remove_issue_component(issue, JiraComponent(name="bau"))
        assert issue.get_field("components") == [self.orderyo_component]

    def test_remove_component_when_value_error(self):
        issue = self.jira_client.get_ticket(self.test_ticket_number)
        self.jira_client.remove_issue_component(issue, JiraComponent(name="bau"))
        assert issue.get_field("components") == [self.orderyo_component]

    def test_append_duplicate_components(self):
        issue = self.jira_client.get_ticket(self.test_ticket_number)
        self.jira_client.append_issue_component(issue, JiraComponent(name="bau"))
        assert issue.get_field("components") == [
            self.test_component,
            self.orderyo_component,
        ]
        self.jira_client.append_issue_component(issue, JiraComponent(name="bau"))
        assert issue.get_field("components") == [
            self.test_component,
            self.orderyo_component,
        ]
