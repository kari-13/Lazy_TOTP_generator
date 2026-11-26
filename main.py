import sys
import getpass

from ansi_ec import ANSI
import ansi_ec

from lazytotp import storage
from lazytotp import oath


class LazyTOTPUI:

    def __init__(self):
        # One storage instance for the entire UI session
        self.store = storage.Storage()
        self.running = True

    # -------------------------
    # Terminal utilities
    # -------------------------

    def clear(self):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    def pause(self):
        try:
            input(f"\n{ANSI.FG_CYAN}Press ENTER to continue...{ANSI.RESET}")
        except (EOFError, KeyboardInterrupt):
            self.running = False

    def header(self, subtitle="Local TOTP Authenticator"):
        self.clear()
        ansi_ec.banner()

        sys.stdout.write(f"\n  {ANSI.FG_CYAN}{subtitle}{ANSI.RESET}\n")
        sys.stdout.write("  " + "-" * 35 + "\n")
        sys.stdout.flush()

    def message(self, text, error=False):
        self.header()

        color = ANSI.FG_RED if error else ANSI.FG_GREEN

        sys.stdout.write(f"\n  {color}{text}{ANSI.RESET}\n")
        sys.stdout.flush()
        self.pause()

    # -------------------------
    # Main menu
    # -------------------------

    def menu(self):

        while self.running:

            try:
                self.header()

                sys.stdout.write(f"""
  {ANSI.BG_BRIGHT_CYAN}{ANSI.FG_BLUE} [1] View Accounts   {ANSI.RESET}
  {ANSI.BG_BLUE}{ANSI.FG_MAGENTA} [2] Add Account     {ANSI.RESET}
  {ANSI.BG_BRIGHT_RED}{ANSI.FG_BRIGHT_YELLOW} [3] Delete Account  {ANSI.RESET}
  {ANSI.BG_MAGENTA}{ANSI.FG_BRIGHT_YELLOW} [4] Generate OTP    {ANSI.RESET}
  {ANSI.BG_RED}{ANSI.FG_BRIGHT_YELLOW} [5] Exit            {ANSI.RESET}\n
""")
                sys.stdout.flush()

                choice = input("  Select an option: ").strip()

                actions = {
                    "1": self.view_accounts,
                    "2": self.add_account,
                    "3": self.delete_account,
                    "4": self.generate_otp,
                    "5": self.exit
                }

                action = actions.get(choice)

                if action:
                    action()
                else:
                    self.message("Invalid menu option.", error=True)

            except (KeyboardInterrupt, EOFError):
                self.exit()

            except Exception as exc:
                self.message(
                    f"Unexpected error: {exc}",
                    error=True
                )

    # -------------------------
    # Account utilities
    # -------------------------

    def check_account(self, name):
        return name in self.store.data

    def get_secret(self, name):
        """
        Retrieves the secret associated with an account.
        Assumes Storage.data maps account names to secret strings.
        """
        return self.store.data.get(name)

    # -------------------------
    # View accounts
    # -------------------------

    def view_accounts(self):

        self.header("Your Accounts")

        accounts = self.store.data

        if not accounts:
            sys.stdout.write("\n  No accounts found.\n")

        else:
            sys.stdout.write(f"\n  Total accounts: {len(accounts)}\n\n")

            for index, (name, secret) in enumerate(
                accounts.items(), start=1
            ):
                masked = "*" * 8
                sys.stdout.write(
                    f"  {index:02}. {name:<22} {masked}\n"
                )

        sys.stdout.flush()
        self.pause()

    # -------------------------
    # Add account
    # -------------------------

    def add_account(self):

        self.header("Add Account")

        name = input("\n  Account name: ").strip()

        if not name:
            self.message("Account name cannot be empty.", True)
            return

        if name in self.store.data:
            self.message("An account with that name already exists.", True)
            return

        secret = getpass.getpass(
            "  TOTP secret: "
        ).strip().replace(" ", "").upper()

        if not secret:
            self.message("Secret cannot be empty.", True)
            return

        # Validate Base32 encoding before saving
        try:
            oath._sanitize_and_decode_base32(secret)
        except Exception:
            self.message("Invalid Base32 TOTP secret.", True)
            return

        try:
            self.store.add(**{name: secret})
            self.message("Account added successfully.")

        except Exception as exc:
            self.message(f"Could not add account: {exc}", True)

    # -------------------------
    # Delete account
    # -------------------------

    def delete_account(self):

        self.header("Delete Account")

        name = input("\n  Account name: ").strip()

        if not name:
            self.message("Account name cannot be empty.", True)
            return

        if not self.check_account(name):
            self.message("Account does not exist.", True)
            return

        confirm = input(
            f"\n  Delete '{name}'? (y/N): "
        ).strip().lower()

        if confirm != "y":
            self.message("Deletion cancelled.")
            return

        try:
            self.store.remove(name)
            self.message("Account deleted successfully.")

        except Exception as exc:
            self.message(f"Deletion failed: {exc}", True)

    # -------------------------
    # Generate OTP
    # -------------------------

    def generate_otp(self):

        self.header("Generate OTP")

        name = input("\n  Account name: ").strip()

        if not name:
            self.message("Account name cannot be empty.", True)
            return

        if not self.check_account(name):
            self.message("Account does not exist.", True)
            return

        secret = self.get_secret(name)

        if not secret:
            self.message("Account has no valid secret.", True)
            return

        try:
            otp = oath.totp_generate(secret)

            sys.stdout.write(f"\n  Account : {name}\n")
            sys.stdout.write(f"  OTP     : {ANSI.FG_GREEN}{otp}{ANSI.RESET}\n")
            sys.stdout.flush()

            self.pause()

        except Exception as exc:
            self.message(f"OTP generation failed: {exc}", True)

    # -------------------------
    # Exit
    # -------------------------

    def exit(self):

        self.running = False

        self.header()

        sys.stdout.write(
            f"\n  {ANSI.FG_GREEN}Vault session closed.{ANSI.RESET}\n\n"
        )
        sys.stdout.flush()


if __name__ == "__main__":

    try:
        ui = LazyTOTPUI()
        ui.menu()

    except KeyboardInterrupt:
        sys.stdout.write("\n\nSession interrupted.\n")
        sys.stdout.flush()

    except Exception as exc:
        sys.stdout.write(f"\nFatal error: {exc}\n")
        sys.stdout.flush()
        sys.exit(1)
