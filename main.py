import os
import traceback

import requests  # noqa We are just importing this to prove the dependency installed correctly

from apps.jira_clients import JiraClient


def get_target_branches(branch_name: str) -> list:
    if "," in branch_name:
        return branch_name.split(",")
    return [branch_name]


def main():
    # my_input = os.environ["INPUT_MYINPUT"]

    # set client
    jira_user = os.environ["JIRA_USER"]
    jira_password = os.environ["JIRA_PASSWORD"]
    jira_server = os.environ["JIRA_SERVER"]

    jira_client = JiraClient(jira_user, jira_password, {"server": jira_server})

    # Input
    target_branches = get_target_branches(os.environ["INPUT_BRANCHNAME"])
    label_to_add = os.environ["INPUT_LABELTOADD"]
    label_to_remove = os.environ["INPUT_LABELTOREMOVE"]
    component_to_add = os.environ["INPUT_COMPONENTTOADD"]
    component_to_remove = os.environ["INPUT_COMPONENTTOREMOVE"]

    # Output
    currentLinkedIssue = []

    for branch in target_branches:
        try:
            issue = jira_client.find_issue_from_branch_name(branch)
            if label_to_add:
                jira_client.append_issue_label(issue, label_to_add)
            if label_to_remove:
                jira_client.remove_issue_label(issue, label_to_remove)
            if component_to_add:
                jira_client.append_issue_component(issue, component_to_add)
            if component_to_remove:
                jira_client.remove_issue_component(issue, component_to_remove)
            currentLinkedIssue.append(
                {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "labels": issue.fields.labels,
                    "components": issue.fields.components,
                    "links": jira_client.get_linked_issues(issue),
                }
            )
        except Exception:
            print(traceback.format_exc())
            continue

    command = f"echo 'myOutput={currentLinkedIssue}' >> $GITHUB_OUTPUT"
    os.system(command)


if __name__ == "__main__":
    main()
