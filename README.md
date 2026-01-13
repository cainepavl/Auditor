# Credential Exposure Auditor 🛡️

A privacy-centric security tool developed in Python to audit passwords against known data breaches. This application utilizes the **Have I Been Pwned (HIBP) API** and implements the **k-Anonymity** model to ensure that sensitive credentials never leave the local environment.

## 🔒 Security & Privacy Architecture

This project was built with a "Security-First" mindset, focusing on mitigating the risks associated with handling plain-text credentials.

* **k-Anonymity Protocol:** The auditor generates a SHA-1 hash of the input but only transmits the first 5 characters (the prefix) to the API. The full hash and plain-text password are never exposed to the network.
* **Zero-Trace Input:** By utilizing the getpass module, the tool prevents passwords from being echoed to the terminal screen and ensures they are not logged in the shell's command history (.bash_history / .zsh_history).
* **Local Hash Comparison:** The script performs a local comparison of the hash "suffix" against the API's anonymized response, ensuring 100% privacy from the service provider.

## 🛠️ Features
* **Breach Frequency Analysis:** Identifies exactly how many times a credential has appeared in public data leaks.
* **Cross-Platform UI:** Uses colorama for clear, color-coded terminal alerts (Red for compromised, Green for secure).
* **Input Masking:** Secure prompt handling to prevent "shoulder surfing" in office environments.
* **Graceful Exception Handling:** Designed to exit securely on user interruption (Ctrl+C).

## 🚀 Installation & Usage

### Prerequisites
* Python 3.x
* requests
* colorama

### Setup
1. Clone the repository:
   git clone https://github.com/cainepavl/credential-auditor.git
   cd credential-auditor

2. Install dependencies:
   pip install requests colorama

### Execution
Run the auditor via the terminal:
python3 auditor.py

## 📖 Technical Workflow
1. Hashing: The input is encoded and hashed using the SHA-1 algorithm.
2. Range Query: The first 5 characters are sent to the HIBP "Range" API.
3. Anonymized Response: The API returns a list of all leaked hash suffixes matching that prefix.
4. Local Audit: The script iterates through the list locally to find a match.
5. Risk Report: The tool outputs the total count of exposures found in the HIBP dataset.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📩 Contact
Caine Pavlosky Email: cainepavl@outlook.com
[Portfolio Website: https://www.pythonanywhere.com/user/surelyNot/] 
[LinkedIn: https://linkedin.com/in/cainepavlosky008]
