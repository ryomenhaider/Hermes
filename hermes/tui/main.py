from textual.app import App
from pages.fred_tui import FredTUI
from widgets.tree import MainScreenTree
from widgets.footers import HermesFooter
from widgets.headers import HermesHeader

class Hermes(App):
    
    SCREENS = {
        "fred": FredTUI,
    }

    def compose(self):
        yield HermesHeader()
        yield MainScreenTree()
        yield HermesFooter()

if __name__ == "__main__":
    
    app = Hermes()
    app.run()