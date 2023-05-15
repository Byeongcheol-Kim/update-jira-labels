import os

import pytest
from dotenv import dotenv_values

from main import main


class TestMain:
    @pytest.fixture(autouse=True)
    def _set_up(self):
        self.env = dotenv_values("../.env")
        self.test_ticket_number = self.env.get("TEST_TICKET_NUMBER")
        self.user = self.env.get("JIRA_USER")
        self.password = self.env.get("JIRA_PASSWORD")
        self.options = {"server": self.env.get("JIRA_SERVER")}

    def test_main(self):
        os.environ["JIRA_USER"] = self.env.get("JIRA_USER")
        os.environ["JIRA_PASSWORD"] = self.env.get("JIRA_PASSWORD")
        os.environ["JIRA_SERVER"] = self.env.get("JIRA_SERVER")
        os.environ["INPUT_MYINPUT"] = "test"

        main()
