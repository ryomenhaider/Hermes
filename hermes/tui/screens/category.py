from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class CategoryScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self, category: str) -> None:
        super().__init__()
        self._category = category

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        with Vertical(id="cat-container"):
            yield Static(self._category, id="cat-title")
            yield OptionList(id="source-list")
            yield Static("", id="cat-empty")
        yield HermesFooter()

    def on_mount(self) -> None:
        ol = self.query_one("#source-list", OptionList)
        empty = self.query_one("#cat-empty", Static)
        registry = self.app.registry  # type: ignore[attr-defined]
        sources = registry.get_by_category(self._category)

        if not sources:
            ol.display = False
            empty.update("No sources in this category yet.")
            return

        current_subcat = ""
        for src in sources:
            subcat = src.get("subcategory", "")
            if subcat and subcat != current_subcat:
                current_subcat = subcat
                ol.add_option(Option(f"── {subcat} ──", id=None, disabled=True))
            ol.add_option(Option(f"  {src['name']}", id=src["id"]))
        for i in range(ol.option_count):
            opt = ol.get_option_at_index(i)
            if opt and not opt.disabled:
                ol.highlighted = i
                break

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id is None:
            return
        from hermes.tui.screens.source import SourceScreen
        self.app.push_screen(SourceScreen(source_id=event.option.id))
