from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class SavedQueriesScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("delete", "delete_query", "Delete"),
    ]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        yield OptionList(id="query-list")
        yield Static("", id="queries-empty")
        yield HermesFooter()

    def on_mount(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        ol = self.query_one("#query-list", OptionList)
        empty = self.query_one("#queries-empty", Static)
        ol.clear_options()
        queries = self.app.saved_queries.list_queries()  # type: ignore[attr-defined]
        if not queries:
            ol.display = False
            empty.update("No saved queries. Run a source and save it.")
            return
        ol.display = True
        empty.update("")
        for q in queries:
            src = self.app.registry.get(q["source_id"])  # type: ignore[attr-defined]
            label = q["name"]
            if src:
                label += f"  —  {src['name']}"
            ol.add_option(Option(f"  {label}", id=q["name"]))
        if ol.option_count > 0:
            ol.highlighted = 0

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from hermes.tui.screens.source import SourceScreen
        query = self.app.saved_queries.get(event.option.id)  # type: ignore[attr-defined]
        if query:
            screen = SourceScreen(source_id=query["source_id"])
            self.app.push_screen(screen)

    def action_delete_query(self) -> None:
        ol = self.query_one("#query-list", OptionList)
        highlighted = ol.highlighted
        if highlighted is not None:
            option = ol.get_option_at_index(highlighted)
            self.app.saved_queries.delete(option.id)  # type: ignore[attr-defined]
            self.app.notify(f"Query '{option.id}' deleted")
            self._refresh()
