from unittest.mock import Mock

import pytest

from src.pytest_html.basereport import ReportData
from src.pytest_html.table import Row


class TestReportData:
    @pytest.fixture(autouse=True)
    def _setup_method(self) -> None:
        # pylint: disable=attribute-defined-outside-init
        self.config = Mock()
        self.title = "test_title"
        self.config.getini.return_value = "Html"

    @pytest.mark.parametrize(
        "values, expect",
        [
            ["Html", "html"],
            ["True,False", "false"],
        ],
    )
    def test__handle_render_collapsed__success(self, values, expect):
        self.config.getini.return_value = values
        report = ReportData(self.title, self.config)

        assert report.title == self.title
        assert expect in report.data["collapsed"]

    def test_set_data(self):
        self.config.getini.return_value = "Html"
        report = ReportData(self.title, self.config)
        report.set_data("test_key", 1)

        assert report.data["test_key"] == 1

    @pytest.mark.parametrize(
        "when, longrepr, outcome, expect",
        [
            ["call", "", "", True],
            ["call", "<test>", "", True],
            ["teardown", "", "", True],
            ["teardown", "", "passed", False],
            ["setup", "", "", True],
        ],
    )
    def test_add_test(self, when, longrepr, outcome, expect):
        test_data = {"result": "Passed"}
        row = Row()
        report = Mock(spec=["when", "longreprtext", "sections", "nodeid"])
        report.when = when
        report.longreprtext = longrepr
        report.outcome = outcome
        report.sections = [("header", "test")]

        report_data = ReportData(self.title, self.config)
        res = report_data.add_test(test_data, report, row)

        assert res is expect
