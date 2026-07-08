from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class SourcesScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        with Vertical():
            yield OptionList(id="category-list")
            yield Static("", id="sources-empty")
        yield HermesFooter()

    def on_mount(self) -> None:
        ol = self.query_one("#category-list", OptionList)
        empty = self.query_one("#sources-empty", Static)
        registry = self.app.registry  # type: ignore[attr-defined]
        cats = registry.categories
        if not cats:
            ol.display = False
            empty.update("No sources registered. Create a connector and it will appear here.")
        else:
            for cat in cats:
                ol.add_option(Option(f"  {cat}", id=cat))
            ol.highlighted = 0

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from hermes.tui.screens.category import CategoryScreen
        self.app.push_screen(CategoryScreen(category=event.option.id))
