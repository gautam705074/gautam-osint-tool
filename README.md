# 📧 GAUTAM OSINT TOOL

> **Complete Email Investigation Framework for Security Research**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![OSINT](https://img.shields.io/badge/OSINT-Email-red)](https://osintframework.com/)
[![Kali](https://img.shields.io/badge/Kali-Linux-blueviolet?logo=kalilinux)](https://www.kali.org/)

---

## 📸 Tool Screenshot

```
╔══════════════════════════════════════════════════════════════════╗
║         📧 GAUTAM OSINT TOOL 📧                                ║
║          Complete Email Investigation Framework                  ║
║                                                                  ║
║   🔍 Email → 🕵️ Social → 📍 Location → 📊 Report              ║
╚══════════════════════════════════════════════════════════════════╝

[+] Target: target@gmail.com
[+] Username: target

[*] Validating Email...
[+] Email VALID ✅

[*] Social Media Search...
[+] Instagram: Found ✅
[+] Twitter: Found ✅
[+] GitHub: Found ✅

[*] Data Breaches...
[+] No breaches ✅

[*] Location...
[+] Location ✅
  City: New Delhi
  Country: IN

[*] Generating Report...
[+] JSON: report_target_20260809_120000.json
[+] HTML: report_target_20260809_120000.html

✅ Done!
```

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| ✅ **Email Validation** | Check if email exists and is valid |
| ✅ **Domain Information** | DNS, MX, A, NS, TXT records |
| ✅ **Social Media** | 16+ platforms search |
| ✅ **Gravatar** | Profile photo from Gravatar |
| ✅ **Data Breaches** | HaveIBeenPwned check |
| ✅ **IP Geolocation** | City, Country, Timezone |
| ✅ **Reports** | JSON + HTML reports |
| ✅ **One Command** | Simple and easy to use |

---

## 🚀 Installation

```bash
# Step 1: Clone repository
git clone https://github.com/gautam705074/gautam-osint-tool.git
cd gautam-osint-tool

# Step 2: Run setup
chmod +x setup.sh
./setup.sh

# Step 3: Run tool
python3 gautam_osint.py target@gmail.com
```

---

## 💻 Usage

### Direct Mode
```bash
python3 gautam_osint.py target@gmail.com
```

### Interactive Mode
```bash
python3 gautam_osint.py
# Enter email when prompted
```

---

## 📊 Output Files

| File | Format | Description |
|------|--------|-------------|
| `report_*.json` | JSON | Full structured data |
| `report_*.html` | HTML | Human-readable report |

---

## 📁 Project Structure

```
gautam-osint-tool/
├── gautam_osint.py     # Main tool
├── README.md           # Documentation
├── banner.txt          # GAUTAM banner
├── setup.sh            # Setup script
├── requirements.txt    # Dependencies
└── LICENSE             # MIT License
```

---

## ⚠️ Disclaimer

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ⚠️  THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY          │
│                                                             │
│   ❌ Do not use without proper authorization               │
│   ❌ Do not violate anyone's privacy                       │
│   ❌ Do not use for illegal activities                     │
│   ✅ Use only on your own data or with permission          │
│                                                             │
│   Unauthorized use may violate:                            │
│   - IT Act 2000                                            │
│   - Privacy Laws                                           │
│   - Cyber Crime Laws                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Requirements

- Python 3.x
- dnspython
- requests

---

## 🛡️ Legal Notice

- For **security research** and **educational purposes**
- Always get **written permission** before investigating
- Author is not responsible for misuse

---

## ⭐ Support

If you find this tool useful:
- Give it a ⭐ on GitHub
- Share with friends
- Report issues

---

## 🎯 Quick Commands

```bash
# Setup
git clone https://github.com/gautam705074/gautam-osint-tool.git
cd gautam-osint-tool
./setup.sh

# Run
python3 gautam_osint.py target@gmail.com

# View Report
cat report_*.json | python3 -m json.tool
```

---

**Made with ❤️ by GAUTAM**
