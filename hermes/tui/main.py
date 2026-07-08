from textual.app import App
from widgets.footers import HermesFooter
from widgets.headers import HermesHeader
from widgets.main_menu import MainMenu
class Hermes(App):

    def compose(self):
        yield HermesHeader

        yield MainMenu

        yield HermesFooter

if __name__ == "__main__":
    
    app = Hermes()
    app.run()