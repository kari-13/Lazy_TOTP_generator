# Lazy_TOTP_generator

> A lightweight, local-first TOTP authenticator for the terminal.

LazyTOTP is an open-source desktop authenticator designed for people who want a simple, privacy-friendly way to generate TOTP codes without relying on a smartphone.

It uses **liboath** as its TOTP backend and provides a clean Python interface with an encrypted local vault.

---

## Why?

Many authenticators assume you have a smartphone.

LazyTOTP exists for users who:

* Prefer desktop authentication.
* Don't always have access to a phone.
* Want an open-source solution.
* Want full control over where their encrypted vault is stored.

---

## Features

* 🔐 Local encrypted vault
* 🔢 RFC 6238 compliant TOTP generation
* ⚡ Native `liboath` backend
* 🖥️ Terminal-first interface
* 📁 Bring Your Own Sync (OneDrive, Syncthing, Dropbox, Google Drive, etc.)
* 🌍 Cross-platform design
* 🔓 Fully open source

---

## Project Status

> **Early Development**

Current progress:

* [x] Native `liboath` integration
* [x] TOTP generation
* [ ] Encrypted vault
* [ ] Multiple accounts
* [ ] QR code import
* [ ] Terminal UI
* [ ] Automatic sync support

---

## Installation

```bash
git clone https://github.com/<username>/Lazy_TOTP_generator.git

cd Lazy_TOTP_generator

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Build the native library (instructions coming soon):

```bash
python build.py
```

---

## Usage

```bash
python main.py
```

---

## Security

LazyTOTP stores secrets locally in an encrypted vault.

Planned design:

* Argon2id for key derivation
* AES-GCM or ChaCha20-Poly1305 encryption
* Random salt per vault
* Authentication tags for integrity

Secrets never leave your computer unless **you** choose to synchronize the encrypted vault using your preferred storage provider.

---

## Philosophy

LazyTOTP is built around a few simple principles:

* Your secrets belong to you.
* Offline should be the default.
* No mandatory cloud service.
* No account required.
* Keep dependencies minimal.
* Be transparent.

---

## Roadmap

* Native library wrapper
* Vault encryption
* QR code import
* Multiple account support
* Search
* Clipboard integration
* Automatic updates
* Plugin-based sync providers

---

## Contributing

Bug reports, suggestions, and pull requests are welcome.

Please open an issue before making major changes so the design can be discussed first.

---

## License

This project is open source.

License: *TBD*
