from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class CredentialsScreen(Screen):
    """List of categories — pick one to see sources that need credentials."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        yield OptionList(id="cred-category-list")
        yield Static("", id="cred-cat-empty")
        yield HermesFooter()

    def on_mount(self) -> None:
        ol = self.query_one("#cred-category-list", OptionList)
        empty = self.query_one("#cred-cat-empty", Static)
        registry = self.app.registry  # type: ignore[attr-defined]
        cats = registry.categories
        if not cats:
            ol.display = False
            empty.update("No categories available.")
            return
        for cat in cats:
            ol.add_option(Option(f"  {cat}", id=cat))
        ol.highlighted = 0

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from hermes.tui.screens.cred_sources import CredSourcesScreen
        self.app.push_screen(CredSourcesScreen(category=event.option.id))
