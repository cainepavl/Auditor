# 🕵️ Credential Exposure Auditor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![HIBP API](https://img.shields.io/badge/HIBP_API-Integrated-D9534F?style=for-the-badge)
![Privacy](https://img.shields.io/badge/k--Anonymity-Protected-7c3aed?style=for-the-badge&logo=gnuprivacyguard&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-64748b?style=for-the-badge)

</div>

<br>

<div align="center">
  <img src="assets/auditor.png" alt="Credential Exposure Auditor in action" width="720"/>
</div>

<br>

A privacy-centric command-line tool for security engineers, sysadmins, and developers who need to audit credentials against known breach data — without sending a password anywhere. Built for people who live in the terminal and want a tool that fits into their existing workflows.

---

## 📋 Table of Contents

- [Security and Privacy Architecture](#security-and-privacy-architecture)
- [Features](#features)
- [Why CLI?](#why-cli)
- [Installation](#installation)
- [WSL (Windows Subsystem for Linux)](#wsl-windows-subsystem-for-linux)
- [Usage](#usage)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Technical Workflow](#technical-workflow)
- [License](#license)
- [Contact/Connect](#contactconnect)

---

## 🔒 Security and Privacy Architecture

This project was built with a "Security-First" mindset, focusing on mitigating the risks associated with handling plain-text credentials.

* **k-Anonymity Protocol:** The auditor generates a SHA-1 hash of the input but only transmits the first 5 characters (the prefix) to the API. The full hash and plain-text password are never exposed to the network.
* **Zero-Trace Input:** By utilizing the `getpass` module, the tool prevents passwords from being echoed to the terminal screen and ensures they are not logged in the shell's command history (`.bash_history` / `.zsh_history`).
* **Local Hash Comparison:** The script performs a local comparison of the hash suffix against the API's anonymized response, ensuring 100% privacy from the service provider.

> **Note:** A clean result means this credential has not appeared in known breach data — it does not assess password strength. A password can pass this audit and still be weak.

---

## ✨ Features

* **Breach Frequency Analysis:** Identifies exactly how many times a credential has appeared in public data leaks.
* **Cross-Platform UI:** Uses `colorama` for clear, color-coded terminal alerts — Red for compromised, Green for secure.
* **Input Masking:** Secure prompt handling to prevent shoulder-surfing in office environments.
* **Graceful Exception Handling:** Designed to exit securely on user interruption (`Ctrl+C`).
* **Scriptable by design:** No GUI, no dependencies on a display — pipe it, schedule it, wrap it. CLI is the right interface for a security tool.

---

## 💻 Why CLI?

Security tools belong in the terminal. This is an intentional design choice, not a limitation:

* **Audience fit** — sysadmins, security engineers, and developers already work here. A desktop window would get in the way.
* **Composability** — CLI tools can be scripted, piped, and slotted into audit pipelines. A GUI locks you to point-and-click.
* **No bloat** — `getpass` and `colorama` are the only UX dependencies. There's nothing to install, configure, or render.

---

## 🛠️ Installation

### 🐍 Verify Python

```bash
python3 --version
# Requires Python 3.x
```

### 📥 Clone the Repository

```bash
git clone https://github.com/cainepavl/Auditor.git
cd Auditor
```

### 📦 Virtual Environment (optional)

```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS / WSL
# venv\Scripts\activate       # Windows (native CMD)
```

### ⬇️ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🐧 WSL (Windows Subsystem for Linux)

This tool is pure CLI with no GUI requirements — it runs in WSL without any extra display setup. Simply open a WSL terminal and follow the standard installation steps above.

---

## 🚀 Usage

```bash
python3 CredExpoAud.py
```

The tool prompts for a password (input is masked — nothing is echoed to the terminal), then checks it against the HIBP Range API and displays the result with color-coded output.

---

## 🧪 Testing & Quality Assurance

The test suite covers all core logic without making any real network calls — every API interaction is mocked, so tests run fully offline.

```bash
python3 -m unittest test -v
```

**17 tests across 4 classes:**

| Class | What It Covers |
|---|---|
| `TestGetPasswordLeaksCount` | Match found, no match, first/last entry edge cases, empty response, case sensitivity |
| `TestRequestApiData` | Successful 200 response with correct URL, non-200 raises `RuntimeError` with status code |
| `TestPwnedApiCheck` | Pwned password returns count, clean password returns 0, prefix length exactly 5, prefix always uppercase |
| `TestMain` | Empty input aborts cleanly, pwned and clean passwords both complete with exit code 0 |

**Privacy guarantees verified by tests:**

* `test_only_prefix_sent_to_api` — confirms only the first 5 characters of the SHA-1 hash are ever passed to the API. The full hash and plain-text password never leave the local environment.
* `test_prefix_is_exactly_5_chars` — enforces the 5-character boundary of the k-Anonymity model.
* `test_hash_prefix_is_uppercase` — confirms the prefix matches the uppercase format required by the HIBP Range API.

---

## 🔍 Technical Workflow

1. **Hashing** — The input is encoded and hashed using the SHA-1 algorithm.
2. **Range Query** — The first 5 characters of the hash are sent to the HIBP Range API.
3. **Anonymized Response** — The API returns all leaked hash suffixes matching that prefix.
4. **Local Audit** — The script iterates through the list locally to find a match.
5. **Risk Report** — The tool outputs the total count of exposures found in the HIBP dataset.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📩 Contact/Connect

**Caine Pavlosky**

* Email: [cainepavl@outlook.com](mailto:cainepavl@outlook.com)
* Portfolio: [fairdinkumstudios.com](https://fairdinkumstudios.com/)
* LinkedIn: [linkedin.com/in/cainepavlosky008](https://linkedin.com/in/cainepavlosky008)
