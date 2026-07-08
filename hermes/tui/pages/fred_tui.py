from textual.screen import Screen
from textual.widgets import (
    Button,
    Header,
    Footer,
    RichLog,
    Static,
)
from textual.containers import Vertical



class FredTUI(Screen):

    BINDINGS = [
        ("a", "authenticate", "Authenticate"),
        ("f", "fetch", "Fetch"),
        ("v", "validate", "Validate"),
        ("t", "transform", "Transform"),
        ("e", "export", "Export"),
        ("h", "health", "Health"),
    ]

    def compose(self):
        yield Header()

        with Vertical():
            yield Static("FRED Connector", id="title")

            yield Button("Authenticate", id="authenticate")
            yield Button("Validate Credentials", id="validate_credentials")
            yield Button("Fetch", id="fetch")
            yield Button("Validate", id="validate")
            yield Button("Transform", id="transform")
            yield Button("Export", id="export")
            yield Button("Health Check", id="health_check")

            yield RichLog(id="logs")

        yield Footer()

    def on_mount(self):
        self.log_message("FRED TUI Loaded")

        # self.connector = FredConnector()

    def log_message(self, message: str):
        self.query_one("#logs", RichLog).write(message)

    def on_button_pressed(self, event: Button.Pressed):

        actions = {
            "authenticate": self.authenticate,
            "validate_credentials": self.validate_credentials,
            "fetch": self.fetch,
            "validate": self.validate,
            "transform": self.transform,
            "export": self.export,
            "health_check": self.health_check,
        }

        action = actions.get(event.button.id)

        if action:
            action()

    # ------------------------
    # Connector Actions
    # ------------------------

    def authenticate(self):
        self.log_message("Authenticating...")
        # self.connector.authenticate()

    def validate_credentials(self):
        self.log_message("Validating credentials...")
        # self.connector.validate_credentials()

    def fetch(self):
        self.log_message("Fetching data...")
        # self.connector.fetch()

    def validate(self):
        self.log_message("Validating data...")
        # self.connector.validate()

    def transform(self):
        self.log_message("Transforming data...")
        # self.connector.transform()

    def export(self):
        self.log_message("Exporting data...")

    def health_check(self):
        self.log_message("Running health check...")


    def action_authenticate(self):
        self.authenticate()

    def action_fetch(self):
        self.fetch()

    def action_validate(self):
        self.validate()

    def action_transform(self):
        self.transform()

    def action_export(self):
        self.export()

    def action_health(self):
        self.health_check()