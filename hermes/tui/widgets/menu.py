from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option


class HermesMenu(Vertical):
    """Reusable menu with title and options."""

    def __init__(self, title: str = "", options: list[Option] | None = None) -> None:
        super().__init__()
        self._menu_title = title
        self._options = options or []

    def compose(self) -> ComposeResult:
        if self._menu_title:
            with Center():
                yield Static(self._menu_title, id="menu-title")
        with Center():
            yield OptionList(*self._options, id="menu-list")

    @property
    def option_list(self) -> OptionList:
        return self.query_one("#menu-list", OptionList)

    def update_options(self, options: list[Option]) -> None:
        self.option_list.clear_options()
        for opt in options:
            self.option_list.add_option(opt)


class MenuScreen:
    """Mix-in for screens that use the common menu pattern."""
