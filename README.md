# Credential Exposure Auditor

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

A privacy-centric security tool developed in Python to audit passwords against known data breaches. This application utilizes the **Have I Been Pwned (HIBP) API** and implements the **k-Anonymity** model to ensure that sensitive credentials never leave the local environment.

---

## 🔒 Security and Privacy Architecture

This project was built with a "Security-First" mindset, focusing on mitigating the risks associated with handling plain-text credentials.

* **k-Anonymity Protocol:** The auditor generates a SHA-1 hash of the input but only transmits the first 5 characters (the prefix) to the API. The full hash and plain-text password are never exposed to the network.
* **Zero-Trace Input:** By utilizing the `getpass` module, the tool prevents passwords from being echoed to the terminal screen and ensures they are not logged in the shell's command history (`.bash_history` / `.zsh_history`).
* **Local Hash Comparison:** The script performs a local comparison of the hash suffix against the API's anonymized response, ensuring 100% privacy from the service provider.

---

## 🛠️ Features

* **Breach Frequency Analysis:** Identifies exactly how many times a credential has appeared in public data leaks.
* **Cross-Platform UI:** Uses `colorama` for clear, color-coded terminal alerts — Red for compromised, Green for secure.
* **Input Masking:** Secure prompt handling to prevent shoulder-surfing in office environments.
* **Graceful Exception Handling:** Designed to exit securely on user interruption (`Ctrl+C`).

---

## 🚀 Installation & Usage

### Prerequisites

* Python 3.x
* `requests`
* `colorama`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/cainepavl/Auditor.git
   cd Auditor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution

```bash
python3 CredExpoAud.py
```

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

## 📖 Technical Workflow

1. **Hashing** — The input is encoded and hashed using the SHA-1 algorithm.
2. **Range Query** — The first 5 characters of the hash are sent to the HIBP Range API.
3. **Anonymized Response** — The API returns all leaked hash suffixes matching that prefix.
4. **Local Audit** — The script iterates through the list locally to find a match.
5. **Risk Report** — The tool outputs the total count of exposures found in the HIBP dataset.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📩 Contact

**Caine Pavlosky**

* Email: [cainepavl@outlook.com](mailto:cainepavl@outlook.com)
* Portfolio: [pythonanywhere.com/user/surelyNot](https://www.pythonanywhere.com/user/surelyNot/)
* LinkedIn: [linkedin.com/in/cainepavlosky008](https://linkedin.com/in/cainepavlosky008)
