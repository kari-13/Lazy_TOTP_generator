from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Button,
    Input,
    Label,
    Static,
    ListView,
    ListItem,
)


class WelcomeScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="welcome"):
            yield Static("LAZY TOTP", classes="title")
            yield Static("Your codes. Your machine.", classes="subtitle")

            yield Button(
                "Unlock Vault",
                id="unlock",
                variant="primary",
            )

            yield Button(
                "Create Vault",
                id="create",
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "unlock":
            self.app.push_screen("login")

        elif event.button.id == "create":
            self.app.push_screen("create")


class LoginScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="login"):
            yield Label("Unlock Vault", classes="heading")

            yield Input(
                placeholder="Master password",
                password=True,
                id="password",
            )

            yield Button(
                "Unlock",
                variant="primary",
                id="login-button",
            )

            yield Button("Back", id="back")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "login-button":
            self.app.switch_screen("dashboard")

        elif event.button.id == "back":
            self.app.switch_screen("welcome")


class CreateScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="login"):
            yield Label("Create Vault", classes="heading")

            yield Input(
                placeholder="Create master password",
                password=True,
            )

            yield Input(
                placeholder="Confirm password",
                password=True,
            )

            yield Button(
                "Create",
                variant="primary",
                id="create-button",
            )

            yield Button("Back", id="back")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "create-button":
            self.app.switch_screen("dashboard")

        elif event.button.id == "back":
            self.app.switch_screen("welcome")


class DashboardScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="dashboard"):

            yield Static("MY ACCOUNTS", classes="heading")

            yield Input(
                placeholder="Search accounts...",
                id="search",
            )

            yield ListView(
                ListItem(Label("GitHub")),
                ListItem(Label("Google")),
                ListItem(Label("Microsoft")),
                id="accounts",
            )

            with Horizontal(id="actions"):
                yield Button(
                    "+ Add Account",
                    variant="primary",
                    id="add",
                )

                yield Button(
                    "Lock",
                    id="lock",
                )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add":
            self.app.push_screen("add")

        elif event.button.id == "lock":
            self.app.switch_screen("welcome")

    def on_list_view_selected(self, event: ListView.Selected):
        self.app.push_screen("account")


class AccountScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="account-detail"):
            yield Static("GitHub", classes="heading")

            yield Static(
                "123 456",
                id="totp-code",
            )

            yield Static(
                "Expires in 24 seconds",
                classes="subtitle",
            )

            yield Button(
                "Back",
                id="back",
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()


class AddAccountScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="login"):
            yield Label("Add Account", classes="heading")

            yield Input(
                placeholder="Account name",
            )

            yield Input(
                placeholder="Issuer",
            )

            yield Input(
                placeholder="Secret key",
                password=True,
            )

            yield Button(
                "Save Account",
                variant="primary",
                id="save",
            )

            yield Button(
                "Cancel",
                id="cancel",
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id in ("save", "cancel"):
            self.app.pop_screen()


class LazyTOTP(App):

    CSS_PATH = "styles.tcss"

    TITLE = "LazyTOTP"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self):
        self.install_screen(WelcomeScreen(), "welcome")
        self.install_screen(LoginScreen(), "login")
        self.install_screen(CreateScreen(), "create")
        self.install_screen(DashboardScreen(), "dashboard")
        self.install_screen(AccountScreen(), "account")
        self.install_screen(AddAccountScreen(), "add")

        self.push_screen("welcome")


if __name__ == "__main__":
    LazyTOTP().run()
