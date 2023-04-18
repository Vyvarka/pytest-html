import re
import warnings
from dataclasses import dataclass
from dataclasses import field


@dataclass
class Table:
    _html: field = field(default_factory=dict)

    @property
    def html(self):
        return self._html


@dataclass
class Html(Table):
    _replace_log: bool = False

    def __post_init__(self):
        self.html.setdefault("html", [])

    def __delitem__(self, key):
        # This means the log should be removed
        self._replace_log = True

    @property
    def replace_log(self) -> bool:
        return self._replace_log

    def append(self, html):
        self.html["html"].append(html)


@dataclass
class Cell(Table):
    _append_counter: int = 0
    _pop_counter: int = 0
    _sortables: field = field(default_factory=dict)

    def __setitem__(self, key, value):
        warnings.warn(
            "list-type assignment is deprecated and support "
            "will be removed in a future release. "
            "Please use 'insert()' instead.",
            DeprecationWarning,
        )
        self.insert(key, value)

    @property
    def sortables(self):
        return self._sortables

    def append(self, item):
        # We need a way of separating inserts from appends in JS,
        # hence the "Z" prefix
        self.insert(f"Z{self._append_counter}", item)
        self._append_counter += 1

    def insert(self, index, html):
        # backwards-compat
        if not isinstance(html, str):
            html = self.check_html(html=html)

        self._extract_sortable(html)
        self._html[index] = html

    @staticmethod
    def check_html(html):
        if html.__module__.startswith("py."):
            warnings.warn(
                "The 'py' module is deprecated and support "
                "will be removed in a future release.",
                DeprecationWarning,
            )
        html = str(html)
        html = html.replace("col=", "data-column-type=")
        return html

    def pop(self, *args):
        self._pop_counter += 1

    def get_pops(self):
        return self._pop_counter

    def _extract_sortable(self, html):
        match = re.search(r'<td class="col-(\w+)">(.*?)</', html)
        if match:
            sortable = match.group(1)
            value = match.group(2)
            self._sortables[sortable] = value


@dataclass
class Header(Cell):
    pass


@dataclass
class Row(Cell):
    def __delitem__(self, key):
        # This means the item should be removed
        self._html = None

    def pop(self, *args):
        # Calling pop on header is sufficient
        pass
