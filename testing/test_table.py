from collections import defaultdict
from unittest.mock import Mock

import pytest

from pytest_html.table import Cell
from pytest_html.table import Html


class TestHtml:
    def test_append(self):
        table = Html()
        table.append("test")

        assert "test" in table.html["html"]
        assert not table.replace_log


class TestCell:
    def test_append(self):
        table = Mock(_append_counter=0, spec=["insert"])
        Cell.append(table, "test")

        assert table._append_counter
        assert table.insert.call_count == 1
        assert "test" in table.insert.call_args.args

    @pytest.mark.parametrize(
        "value, call_check, expect",
        [
            ["test", False, "test"],
            [1, True, "data-column-type="],
        ],
    )
    def test_insert(self, value, call_check, expect):
        table = Mock(_html=defaultdict(), spec=["check_html", "_extract_sortable"])
        table.check_html.return_value = "data-column-type="
        Cell.insert(table, "0", value)

        assert table.check_html.called is call_check
        assert table._html["0"] == expect

    def test_pop(self):
        table = Mock(_pop_counter=0)
        Cell.pop(table, *["test", "html"])

        assert table._pop_counter == 1

    def test_get_pops(self):
        table = Cell()
        table.pop("test")

        assert table.get_pops() == 1
