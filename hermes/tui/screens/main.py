from __future__ import annotations

import pyfiglet
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option

from hermes.tui.widgets.header import HermesHeader
from hermes.tui.widgets.footer import HermesFooter


class MainMenu(Screen):
    BINDINGS = [
        ("d", "go_sources", "Data Sources"),
        ("c", "go_credentials", "Credentials"),
        ("q", "go_saved_queries", "Saved Queries"),
        ("j", "go_jobs", "Jobs"),
        ("s", "go_settings", "Settings"),
    ]

    def compose(self) -> ComposeResult:
        yield HermesHeader()
        banner = pyfiglet.figlet_format("HERMES", font="slant")
        with Vertical():
            with Center():
                yield Static(banner, id="banner")
            yield Static("Universal Data Acquisition Platform", id="subtitle")
            with Center():
                yield OptionList(
                    Option("  Data Sources", id="sources"),
                    Option("  Credentials", id="credentials"),
                    Option("  Saved Queries", id="saved_queries"),
                    Option("  Jobs", id="jobs"),
                    Option("  Settings", id="settings"),
                    Option("  Exit", id="exit"),
                    id="menu",
                )
        yield HermesFooter()

    def on_mount(self) -> None:
        self.query_one("#menu", OptionList).highlighted = 0

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        choice = event.option.id
        if choice == "exit":
            self.app.exit()
        elif choice == "sources":
            self.app.push_screen(self._make_sources())
        elif choice == "credentials":
            self.app.push_screen(self._make_credentials())
        elif choice == "saved_queries":
            self.app.push_screen(self._make_saved_queries())
        elif choice == "jobs":
            self.app.push_screen(self._make_jobs())
        elif choice == "settings":
            self.app.push_screen(self._make_settings())

    def _make_sources(self):
        from hermes.tui.screens.sources import SourcesScreen
        return SourcesScreen()

    def _make_credentials(self):
        from hermes.tui.screens.credentials import CredentialsScreen
        return CredentialsScreen()

    def _make_saved_queries(self):
        from hermes.tui.screens.saved_queries import SavedQueriesScreen
        return SavedQueriesScreen()

    def _make_jobs(self):
        from hermes.tui.screens.jobs import JobsScreen
        return JobsScreen()

    def _make_settings(self):
        from hermes.tui.screens.settings import SettingsScreen
        return SettingsScreen()

    def action_go_sources(self) -> None:
        self.app.push_screen(self._make_sources())

    def action_go_credentials(self) -> None:
        self.app.push_screen(self._make_credentials())

    def action_go_saved_queries(self) -> None:
        self.app.push_screen(self._make_saved_queries())

    def action_go_jobs(self) -> None:
        self.app.push_screen(self._make_jobs())

    def action_go_settings(self) -> None:
        self.app.push_screen(self._make_settings())
