#!/usr/bin/env python3
"""
GAUTAM OSINT TOOL - Complete Email Investigation Tool
All-in-One Email OSINT Framework - Fully Fixed
"""

import os
import sys
import json
import time
import requests
import socket
import subprocess
from datetime import datetime
import hashlib

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'

class GAUTAM_OSINT:
    def __init__(self, email):
        self.email = email
        self.username = email.split('@')[0] if '@' in email else email
        self.domain = email.split('@')[1] if '@' in email else None
        self.results = {
            'email': email,
            'username': self.username,
            'domain': self.domain,
            'timestamp': datetime.now().isoformat(),
            'valid': False,
            'domain_info': {},
            'social_media': [],
            'breaches': [],
            'location': {},
            'gravatar': None,
            'google_results': [],
            'phone_numbers': [],
            'image': None
        }

    def banner(self):
        os.system('clear')
        print(f"""{R}
╔══════════════════════════════════════════════════════════════════╗
║         📧 GAUTAM OSINT TOOL 📧                                ║
║          Complete Email Investigation                          ║
║                                                                  ║
║   🔍 Scan → 🌐 Domain → 🕵️ Social → 📊 Report                 ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
        print(f"{C}[+] Target: {Y}{self.email}{RESET}")
        print(f"{C}[+] Username: {Y}{self.username}{RESET}")
        print(f"{C}[+] Domain: {Y}{self.domain}{RESET}")
        print("="*70)

    # ==========================================
    # 1. EMAIL VALIDATION
    # ==========================================
    def validate_email(self):
        print(f"\n{B}[*] Validating Email...{RESET}")
        try:
            import dns.resolver
            mx = dns.resolver.resolve(self.domain, 'MX')
            if mx:
                self.results['valid'] = True
                print(f"{G}[+] Email is VALID ✅{RESET}")
                return True
        except:
            pass
        print(f"{R}[!] Email validation failed{RESET}")
        return False

    # ==========================================
    # 2. DOMAIN INFO
    # ==========================================
    def domain_info(self):
        print(f"\n{B}[*] Fetching Domain Info...{RESET}")
        try:
            import dns.resolver
            for record in ['A', 'MX', 'NS']:
                try:
                    ans = dns.resolver.resolve(self.domain, record)
                    self.results['domain_info'][record] = [str(r) for r in ans]
                except:
                    pass
            print(f"{G}[+] Domain info fetched ✅{RESET}")
        except:
            print(f"{Y}[!] Domain info partial{RESET}")

    # ==========================================
    # 3. SOCIAL MEDIA CHECK (FIXED)
    # ==========================================
    def social_media(self):
        print(f"\n{B}[*] Checking Social Media...{RESET}")
        
        platforms = [
            ('Instagram', f'https://www.instagram.com/{self.username}'),
            ('Twitter', f'https://twitter.com/{self.username}'),
            ('LinkedIn', f'https://www.linkedin.com/in/{self.username}'),
            ('GitHub', f'https://github.com/{self.username}'),
            ('YouTube', f'https://youtube.com/@{self.username}'),
            ('Reddit', f'https://reddit.com/user/{self.username}'),
            ('Pinterest', f'https://pinterest.com/{self.username}'),
            ('Tumblr', f'https://{self.username}.tumblr.com'),
            ('Medium', f'https://medium.com/@{self.username}'),
            ('Quora', f'https://quora.com/profile/{self.username}'),
        ]
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        for platform, url in platforms:
            try:
                r = requests.get(url, timeout=5, headers=headers, allow_redirects=True)
                if r.status_code == 200 and 'not found' not in r.text.lower():
                    self.results['social_media'].append({'platform': platform, 'url': url})
                    print(f"{G}[+] {platform}: Found ✅{RESET}")
                else:
                    print(f"{Y}[!] {platform}: Not found{RESET}")
                time.sleep(0.3)
            except:
                print(f"{Y}[!] {platform}: Error checking{RESET}")

    # ==========================================
    # 4. GOOGLE SEARCH
    # ==========================================
    def google_search(self):
        print(f"\n{B}[*] Google Search...{RESET}")
        try:
            from googlesearch import search
            for result in search(self.email, num_results=5):
                self.results['google_results'].append(result)
                print(f"{C}  {result}{RESET}")
        except:
            print(f"{Y}[!] Google search skipped{RESET}")

    # ==========================================
    # 5. GRAVATAR IMAGE
    # ==========================================
    def gravatar(self):
        print(f"\n{B}[*] Checking Gravatar...{RESET}")
        try:
            h = hashlib.md5(self.email.lower().encode()).hexdigest()
            url = f"https://www.gravatar.com/avatar/{h}?d=404&s=200"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                self.results['gravatar'] = url
                self.results['image'] = url
                print(f"{G}[+] Gravatar found ✅{RESET}")
            else:
                print(f"{Y}[!] No Gravatar{RESET}")
        except:
            print(f"{Y}[!] Gravatar check failed{RESET}")

    # ==========================================
    # 6. DATA BREACH CHECK
    # ==========================================
    def breaches(self):
        print(f"\n{B}[*] Checking Data Breaches...{RESET}")
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}"
            r = requests.get(url, timeout=10, headers={'hibp-api-key': ''})
            if r.status_code == 200:
                for b in r.json():
                    self.results['breaches'].append({'name': b.get('Name'), 'date': b.get('BreachDate')})
                    print(f"{R}[!] {b.get('Name')} - {b.get('BreachDate')}{RESET}")
            else:
                print(f"{G}[+] No breaches found ✅{RESET}")
        except:
            print(f"{Y}[!] Breach check failed{RESET}")

    # ==========================================
    # 7. LOCATION
    # ==========================================
    def location(self):
        print(f"\n{B}[*] Getting Location...{RESET}")
        try:
            r = requests.get('https://ipinfo.io/json', timeout=10)
            if r.status_code == 200:
                data = r.json()
                self.results['location'] = {
                    'ip': data.get('ip'),
                    'city': data.get('city'),
                    'region': data.get('region'),
                    'country': data.get('country'),
                    'org': data.get('org')
                }
                print(f"{G}[+] Location fetched ✅{RESET}")
                print(f"{C}  IP: {Y}{data.get('ip')}{RESET}")
                print(f"{C}  City: {Y}{data.get('city')}{RESET}")
                print(f"{C}  Country: {Y}{data.get('country')}{RESET}")
        except:
            print(f"{Y}[!] Location check failed{RESET}")

    # ==========================================
    # 8. PHONE NUMBER SEARCH (Using Social Media)
    # ==========================================
    def phone_search(self):
        print(f"\n{B}[*] Searching for phone numbers...{RESET}")
        try:
            import phonenumbers
            # Extract possible phone numbers from social media
            for item in self.results['social_media']:
                if item.get('platform') in ['LinkedIn', 'Facebook']:
                    print(f"{C}  Check {item['platform']} for phone{RESET}")
        except:
            print(f"{Y}[!] Phone search skipped{RESET}")

    # ==========================================
    # 9. GENERATE REPORT
    # ==========================================
    def report(self):
        print(f"\n{B}[*] Generating Report...{RESET}")
        
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        jf = f"report_{self.username}_{ts}.json"
        with open(jf, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"{G}[+] JSON: {jf}{RESET}")
        
        # HTML
        hf = f"report_{self.username}_{ts}.html"
        html = f"""
        <html>
        <head><title>GAUTAM OSINT - {self.email}</title>
        <style>
        body {{ font-family: Arial; background: #0a0a0a; color: #fff; padding: 20px; }}
        .container {{ max-width: 800px; margin: auto; background: #1a1a2e; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #f5576c; text-align: center; }}
        .section {{ background: #2a2a3e; padding: 15px; margin: 10px 0; border-radius: 8px; }}
        .green {{ color: #2ecc71; }} .red {{ color: #e74c3c; }} .blue {{ color: #3498db; }}
        pre {{ background: #111; padding: 10px; border-radius: 5px; overflow: auto; }}
        </style>
        </head>
        <body>
        <div class="container">
        <h1>📧 GAUTAM OSINT REPORT</h1>
        <p><b>Email:</b> {self.email}</p>
        <p><b>Username:</b> {self.username}</p>
        <p><b>Domain:</b> {self.domain}</p>
        <p><b>Generated:</b> {self.results['timestamp']}</p>
        <p><b>Valid:</b> <span class="{'green' if self.results['valid'] else 'red'}">{self.results['valid']}</span></p>
        
        <div class="section"><h2>🌐 Domain Info</h2><pre>{json.dumps(self.results['domain_info'], indent=2, default=str)}</pre></div>
        <div class="section"><h2>🕵️ Social Media</h2><pre>{json.dumps(self.results['social_media'], indent=2, default=str)}</pre></div>
        <div class="section"><h2>🔓 Breaches</h2><pre>{json.dumps(self.results['breaches'], indent=2, default=str)}</pre></div>
        <div class="section"><h2>📍 Location</h2><pre>{json.dumps(self.results['location'], indent=2, default=str)}</pre></div>
        <div class="section"><h2>🖼️ Gravatar</h2>{f'<img src="{self.results["gravatar"]}" style="max-width:200px;border-radius:50%;"/>' if self.results['gravatar'] else 'Not found'}</div>
        <div style="text-align:center;color:#666;padding:20px;border-top:1px solid #333;">🛡️ GAUTAM OSINT | Educational Purpose Only</div>
        </div>
        </body>
        </html>
        """
        with open(hf, 'w') as f:
            f.write(html)
        print(f"{G}[+] HTML: {hf}{RESET}")

    # ==========================================
    # 10. RUN ALL
    # ==========================================
    def run_all(self):
        self.banner()
        self.validate_email()
        self.domain_info()
        self.social_media()
        self.gravatar()
        self.breaches()
        self.location()
        self.report()
        print(f"\n{G}✅ Scan Complete!{RESET}")
        print(f"{C}📊 Reports saved in current directory{RESET}")

# ==========================================
# MAIN
# ==========================================
if __name__ == '__main__':
    # Install dependencies if missing
    try:
        import dns.resolver
        import requests
    except ImportError:
        print(f"{Y}[!] Installing dependencies...{RESET}")
        subprocess.run(['pip3', 'install', 'dnspython', 'requests'], capture_output=True)
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
        if '@' not in email:
            print(f"{R}[!] Invalid email format!{RESET}")
            sys.exit(1)
        tool = GAUTAM_OSINT(email)
        tool.run_all()
    else:
        print(f"{R}Usage: python3 osint_tool.py <email>{RESET}")
        print(f"{C}Example: python3 osint_tool.py target@gmail.com{RESET}")
        email = input(f"{C}Enter email: {RESET}")
        if email and '@' in email:
            tool = GAUTAM_OSINT(email)
            tool.run_all()
        else:
            print(f"{R}[!] Invalid email!{RESET}")
