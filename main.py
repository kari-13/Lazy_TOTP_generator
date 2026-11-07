
import sys
import getpass
from ansi_ec import ANSI
import ansi_ec
from lazytotp import storage
class LazyTOTPUI:

    def clear(self):
        print("\033[2J\033[H", end="")

    def pause(self):
        input(f"\n{ANSI.FG_CYAN}Press ENTER to continue...{ANSI.RESET}")

    def header(self, subtitle="Local TOTP Authenticator"):
        self.clear()
        ansi_ec.banner()
        print(f"\n  {ANSI.FG_CYAN}{subtitle}{ANSI.RESET}")
    def menu(self):
        while True:
            self.header()

            print(f"""
                {ANSI.BG_BRIGHT_CYAN}{ANSI.FG_BLUE}[1] View Accounts {ANSI.RESET}
                {ANSI.BG_BLUE}{ANSI.FG_MAGENTA}[2] Add Account   {ANSI.RESET}
                {ANSI.BG_BRIGHT_RED}{ANSI.FG_BRIGHT_YELLOW}[3] Delete Account{ANSI.RESET}
                {ANSI.BG_MAGENTA}{ANSI.FG_BRIGHT_YELLOW}[4] Generate OTP  {ANSI.RESET}
                {ANSI.BG_RED}{ANSI.FG_BRIGHT_YELLOW}     [5] Exit    {ANSI.RESET}
""")
            choice = input("  Select an option: ").strip()

            if choice == "1":
                self.view_accounts()
            elif choice == "2":
                self.add_account()
            elif choice == "3":
                self.delete_account()
            elif choice == "4":
                self.generate_otp()
            elif choice == "5":
                self.exit()
                break
            else:
                self.message("Invalid option.", error=True)

    def login(self):
        self.header("Vault Authentication")

        print("  Enter your master password to unlock.")
        password = getpass.getpass(
            f"\n  {ANSI.FG_RED}Master password: {ANSI.RESET}"
        )

        return password

    def first_time_setup(self):
        self.header("Create Vault")

        while True:
            password = getpass.getpass("  Create master password: ")
            confirm = getpass.getpass("  Confirm master password: ")

            if not password:
                self.message("Password cannot be empty.", error=True)
            elif password != confirm:
                self.message("Passwords do not match.", error=True)
            else:
                return password

    def view_accounts(self):
        self.header("Your Accounts")

        with open('vault.json','r') as w:
            w=S

        print("  No accounts to display.")
        self.pause()

    def add_account(self):
        self.header("Add Account")

        name = input("  Account name: ").strip()
        issuer = input("  Issuer: ").strip()
        secret = getpass.getpass("  TOTP secret: ").strip()

        if not name or not secret:
            self.message("Required fields are missing.", error=True)
            return

        # TODO: Send name, issuer and secret to backend

        self.message("Account added successfully.")

    def delete_account(self):
        self.header("Delete Account")

        name = input("  Account name to delete: ").strip()

        if not name:
            self.message("Account name cannot be empty.", error=True)
            return

        storage.Storage.

        self.message("Delete operation requested.")

    def generate_otp(self):
        self.header("Generate OTP")

        name = input("  Account name: ").strip()

        if not name:
            self.message("Account name cannot be empty.", error=True)
            return
        s=storage.Storage()
        try :s.data[f"name"]
        except keyKeyError :


        print("\n  OTP: [Waiting for backend]")
        self.pause()

    def message(self, text, error=False):
        self.header()
        color = ANSI.FG_RED if error else ANSI.FG_GREEN
        print(f"\n  {color}{text}{ANSI.RESET}")
        self.pause()

    def exit(self):
        self.header()
        print(f"\n  {ANSI.FG_GREEN}Vault session closed.{ANSI.RESET}")

    def check_account(n):
        try :s.data[f"n"]
        except KeyError : return False

if __name__ == "__main__":
    ui = LazyTOTPUI()
    ui.menu()
