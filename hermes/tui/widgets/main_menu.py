import pyfiglet
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Static, OptionList
from textual.widgets.option_list import Option

class MainMenu(App):
    CSS = """
    Screen {
        align: center middle;
        background: $background;
    }

    #banner {
        color: $accent;
        text-style: bold;
        width: auto;
        content-align: center middle;
        margin-bottom: 1;
    }

    #menu {
        width: 30;
        height: auto;
        border: none;
        background: transparent;
    }

    OptionList > .option-list--option-highlighted {
        background: $accent 20%;
        color: $accent;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        banner = pyfiglet.figlet_format("HERMES", font="slant")
        with Vertical():
            with Center():
                yield Static(banner, id="banner")
            with Center():
                yield OptionList(
                    Option("Data Sources", id="data_sources"),
                    Option("Credentials", id="credentials"),
                    Option("Saved Queries", id="saved_queries"),
                    Option("Settings", id="settings"),
                    Option("Exit", id="exit"),
                    id="menu",
                )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        choice = event.option.id
        if choice == 'data_sources':
            self.push_screen(MainScreenTree)
        if choice == "exit":
            self.exit()
        else:
            self.notify(f"Selected: {choice}")
            # route to whatever screen/handler you want here

if __name__ == "__main__":
    MainMenu().run()