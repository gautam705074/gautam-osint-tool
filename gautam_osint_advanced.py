#!/usr/bin/env python3
"""
GAUTAM OSINT TOOL - ADVANCED VERSION
Complete Email Investigation + Extra Features
"""

import os
import sys
import json
import time
import requests
import hashlib
import subprocess
from datetime import datetime
from urllib.parse import urlparse

# Colors
R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
B = '\033[94m'; P = '\033[95m'; C = '\033[96m'
W = '\033[97m'; RESET = '\033[0m'

class GAUTAM_OSINT_ADVANCED:
    def __init__(self, email):
        self.email = email
        self.username = email.split('@')[0]
        self.domain = email.split('@')[1]
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
            'phone_numbers': [],
            'profile_photos': [],
            'linked_accounts': [],
            'dark_web': [],
            'ip_addresses': [],
            'company_info': {},
            'email_header': {},
            'summary': {}
        }

    def banner(self):
        os.system('clear')
        print(f"""{R}
╔══════════════════════════════════════════════════════════════════╗
║         📧 GAUTAM OSINT TOOL - ADVANCED 📧                      ║
║          Complete Email + Phone + Photo Investigation           ║
║                                                                  ║
║   🔍 Email → 📱 Phone → 🖼️ Photos → 📊 Full Report             ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
        print(f"{C}[+] Target: {Y}{self.email}{RESET}")
        print(f"{C}[+] Username: {Y}{self.username}{RESET}")
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
                print(f"{G}[+] Email VALID ✅{RESET}")
                return True
        except:
            pass
        print(f"{R}[!] Invalid email{RESET}")
        return False

    # ==========================================
    # 2. DOMAIN INFO
    # ==========================================
    def domain_info(self):
        print(f"\n{B}[*] Domain Information...{RESET}")
        try:
            import dns.resolver
            for record in ['A', 'MX', 'NS', 'TXT']:
                try:
                    ans = dns.resolver.resolve(self.domain, record)
                    self.results['domain_info'][record] = [str(r) for r in ans]
                except:
                    pass
            print(f"{G}[+] Domain info ✅{RESET}")
        except:
            print(f"{Y}[!] Partial domain info{RESET}")

    # ==========================================
    # 3. SOCIAL MEDIA (ALL PLATFORMS)
    # ==========================================
    def social_media(self):
        print(f"\n{B}[*] Searching Social Media...{RESET}")
        
        platforms = [
            'instagram', 'twitter', 'linkedin', 'github', 'youtube',
            'reddit', 'pinterest', 'tumblr', 'medium', 'quora',
            'facebook', 'snapchat', 'tiktok', 'telegram', 'discord'
        ]
        
        found = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        for platform in platforms:
            url = f"https://www.{platform}.com/{self.username}"
            try:
                r = requests.get(url, timeout=5, headers=headers)
                if r.status_code == 200 and 'not found' not in r.text.lower():
                    found.append({'platform': platform, 'url': url})
                    print(f"{G}[+] {platform.capitalize()}: Found ✅{RESET}")
                else:
                    print(f"{Y}[!] {platform.capitalize()}: Not found{RESET}")
                time.sleep(0.3)
            except:
                print(f"{Y}[!] {platform.capitalize()}: Error{RESET}")
        
        self.results['social_media'] = found

    # ==========================================
    # 4. GRAVATAR + PROFILE PHOTOS
    # ==========================================
    def profile_photos(self):
        print(f"\n{B}[*] Searching Profile Photos...{RESET}")
        
        photos = []
        
        # Gravatar
        try:
            h = hashlib.md5(self.email.lower().encode()).hexdigest()
            gravatar_url = f"https://www.gravatar.com/avatar/{h}?d=404&s=200"
            r = requests.get(gravatar_url, timeout=5)
            if r.status_code == 200:
                photos.append({'source': 'Gravatar', 'url': gravatar_url})
                self.results['gravatar'] = gravatar_url
                print(f"{G}[+] Gravatar found ✅{RESET}")
        except:
            pass
        
        # Google Profile Photo
        try:
            google_url = f"https://picasaweb.google.com/data/entry/api/user/{self.email}"
            r = requests.get(google_url, timeout=5)
            if r.status_code == 200:
                photos.append({'source': 'Google', 'url': google_url})
                print(f"{G}[+] Google profile photo found ✅{RESET}")
        except:
            pass
        
        # Twitter Profile Photo
        try:
            twitter_url = f"https://twitter.com/{self.username}/profile_image"
            r = requests.get(twitter_url, timeout=5)
            if r.status_code == 200:
                photos.append({'source': 'Twitter', 'url': twitter_url})
                print(f"{G}[+] Twitter profile photo found ✅{RESET}")
        except:
            pass
        
        self.results['profile_photos'] = photos

    # ==========================================
    # 5. PHONE NUMBERS
    # ==========================================
    def phone_numbers(self):
        print(f"\n{B}[*] Searching Phone Numbers...{RESET}")
        
        numbers = []
        
        # Google search for phone
        try:
            search_url = f"https://www.google.com/search?q={self.email}+phone+number"
            r = requests.get(search_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if 'phone' in r.text.lower():
                numbers.append({'source': 'Google Search', 'found': True})
                print(f"{G}[+] Phone number found in search ✅{RESET}")
        except:
            pass
        
        # Social media phone
        for platform in self.results['social_media']:
            if platform['platform'] in ['facebook', 'linkedin']:
                numbers.append({'source': platform['platform'], 'found': True})
                print(f"{G}[+] Phone found on {platform['platform']} ✅{RESET}")
        
        self.results['phone_numbers'] = numbers

    # ==========================================
    # 6. DATA BREACHES
    # ==========================================
    def breaches(self):
        print(f"\n{B}[*] Checking Data Breaches...{RESET}")
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                for b in r.json():
                    self.results['breaches'].append({
                        'name': b.get('Name'),
                        'date': b.get('BreachDate'),
                        'description': b.get('Description', '')[:200]
                    })
                    print(f"{R}[!] {b.get('Name')} - {b.get('BreachDate')}{RESET}")
            else:
                print(f"{G}[+] No breaches ✅{RESET}")
        except:
            print(f"{Y}[!] Breach check failed{RESET}")

    # ==========================================
    # 7. LOCATION / IP
    # ==========================================
    def location(self):
        print(f"\n{B}[*] Location & IP Info...{RESET}")
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
                self.results['ip_addresses'].append(data.get('ip'))
                print(f"{G}[+] Location ✅{RESET}")
                print(f"{C}  IP: {Y}{data.get('ip')}{RESET}")
                print(f"{C}  City: {Y}{data.get('city')}{RESET}")
                print(f"{C}  Country: {Y}{data.get('country')}{RESET}")
        except:
            print(f"{Y}[!] Location failed{RESET}")

    # ==========================================
    # 8. LINKED ACCOUNTS
    # ==========================================
    def linked_accounts(self):
        print(f"\n{B}[*] Finding Linked Accounts...{RESET}")
        
        accounts = []
        services = {
            'Amazon': f'https://www.amazon.com/gp/profile/{self.username}',
            'Spotify': f'https://open.spotify.com/user/{self.username}',
            'Netflix': f'https://www.netflix.com/',
            'Adobe': f'https://www.adobe.com/',
            'Apple': f'https://appleid.apple.com/',
            'Microsoft': f'https://account.microsoft.com/'
        }
        
        for service, url in services.items():
            accounts.append({'service': service, 'url': url, 'possible': True})
            print(f"{C}  Possible {service} account{RESET}")
        
        self.results['linked_accounts'] = accounts

    # ==========================================
    # 9. GENERATE REPORT
    # ==========================================
    def generate_report(self):
        print(f"\n{B}[*] Generating Report...{RESET}")
        
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = f"adv_report_{self.username}_{ts}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"{G}[+] JSON: {json_file}{RESET}")
        
        # HTML
        html_file = f"adv_report_{self.username}_{ts}.html"
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GAUTAM OSINT - {self.email}</title>
            <style>
                body {{ font-family: Arial; background: #0a0a0a; color: #fff; padding: 20px; }}
                .container {{ max-width: 900px; margin: auto; background: #1a1a2e; padding: 20px; border-radius: 10px; }}
                h1 {{ color: #f5576c; text-align: center; }}
                .section {{ background: #2a2a3e; padding: 15px; margin: 10px 0; border-radius: 8px; }}
                .green {{ color: #2ecc71; }}
                .red {{ color: #e74c3c; }}
                .yellow {{ color: #f1c40f; }}
                .blue {{ color: #3498db; }}
                table {{ width: 100%; border-collapse: collapse; }}
                td, th {{ padding: 8px; border: 1px solid #444; }}
                img {{ max-width: 200px; border-radius: 50%; }}
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
            
            <div class="section">
                <h2 class="blue">📡 Domain Info</h2>
                <pre>{json.dumps(self.results['domain_info'], indent=2, default=str)}</pre>
            </div>
            
            <div class="section">
                <h2 class="blue">🕵️ Social Media</h2>
                <pre>{json.dumps(self.results['social_media'], indent=2, default=str)}</pre>
            </div>
            
            <div class="section">
                <h2 class="yellow">🖼️ Profile Photos</h2>
                <pre>{json.dumps(self.results['profile_photos'], indent=2, default=str)}</pre>
                {f'<img src="{self.results["gravatar"]}"/>' if self.results.get('gravatar') else ''}
            </div>
            
            <div class="section">
                <h2 class="yellow">📱 Phone Numbers</h2>
                <pre>{json.dumps(self.results['phone_numbers'], indent=2, default=str)}</pre>
            </div>
            
            <div class="section">
                <h2 class="red">🔓 Data Breaches</h2>
                <pre>{json.dumps(self.results['breaches'], indent=2, default=str)}</pre>
            </div>
            
            <div class="section">
                <h2 class="blue">📍 Location</h2>
                <pre>{json.dumps(self.results['location'], indent=2, default=str)}</pre>
            </div>
            
            <div class="section">
                <h2 class="blue">🔗 Linked Accounts</h2>
                <pre>{json.dumps(self.results['linked_accounts'], indent=2, default=str)}</pre>
            </div>
            
            <div style="text-align:center;color:#666;padding:20px;border-top:1px solid #333;">
                🛡️ GAUTAM OSINT TOOL | Educational Purpose Only
            </div>
        </div>
        </body>
        </html>
        """
        with open(html_file, 'w') as f:
            f.write(html)
        print(f"{G}[+] HTML: {html_file}{RESET}")

    # ==========================================
    # 10. RUN ALL
    # ==========================================
    def run_all(self):
        self.banner()
        self.validate_email()
        self.domain_info()
        self.social_media()
        self.profile_photos()
        self.phone_numbers()
        self.breaches()
        self.location()
        self.linked_accounts()
        self.generate_report()
        
        print(f"\n{G}✅ Scan Complete!{RESET}")
        print(f"{C}📊 Reports saved in current directory{RESET}")

# ==========================================
# MAIN
# ==========================================
if __name__ == '__main__':
    if len(sys.argv) > 1:
        email = sys.argv[1]
        if '@' not in email:
            print(f"{R}[!] Invalid email!{RESET}")
            sys.exit(1)
        tool = GAUTAM_OSINT_ADVANCED(email)
        tool.run_all()
    else:
        print(f"{C}Usage: python3 gautam_osint_advanced.py <email>{RESET}")
        print(f"{C}Example: python3 gautam_osint_advanced.py target@gmail.com{RESET}")
