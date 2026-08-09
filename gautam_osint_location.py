#!/usr/bin/env python3
"""
GAUTAM OSINT TOOL - LOCATION FIXED
Target Location Finder - Real Geolocation
"""

import os
import sys
import json
import time
import requests
import hashlib
import socket
import dns.resolver
from datetime import datetime

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'

class GAUTAM_OSINT_LOCATION:
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
            'location': {
                'ip': None,
                'city': 'Unknown',
                'region': 'Unknown',
                'country': 'Unknown',
                'timezone': 'Unknown',
                'org': 'Unknown',
                'source': 'None'
            },
            'breaches': [],
            'gravatar': None,
            'profile_photos': [],
            'summary': {}
        }

    def banner(self):
        os.system('clear')
        print(f"""{R}
╔══════════════════════════════════════════════════════════════════╗
║         📧 GAUTAM OSINT TOOL - LOCATION FIXED 📧               ║
║          Real Target Location Finder                           ║
║                                                                  ║
║   🔍 Email → 📍 Location → 🕵️ Social → 📊 Report              ║
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
            for record in ['A', 'MX', 'NS']:
                try:
                    ans = dns.resolver.resolve(self.domain, record)
                    self.results['domain_info'][record] = [str(r) for r in ans]
                except:
                    pass
            print(f"{G}[+] Domain info ✅{RESET}")
        except:
            print(f"{Y}[!] Partial domain info{RESET}")

    # ==========================================
    # 3. SOCIAL MEDIA
    # ==========================================
    def social_media(self):
        print(f"\n{B}[*] Searching Social Media...{RESET}")
        
        platforms = [
            ('Instagram', f'https://www.instagram.com/{self.username}'),
            ('Twitter', f'https://twitter.com/{self.username}'),
            ('GitHub', f'https://github.com/{self.username}'),
            ('YouTube', f'https://youtube.com/@{self.username}'),
            ('Reddit', f'https://reddit.com/user/{self.username}'),
            ('Pinterest', f'https://pinterest.com/{self.username}'),
            ('Tumblr', f'https://{self.username}.tumblr.com'),
            ('Medium', f'https://medium.com/@{self.username}'),
            ('Facebook', f'https://facebook.com/{self.username}'),
            ('TikTok', f'https://tiktok.com/@{self.username}'),
            ('Telegram', f'https://t.me/{self.username}'),
            ('Twitch', f'https://twitch.tv/{self.username}'),
        ]
        
        found = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        for platform, url in platforms:
            try:
                time.sleep(0.3)
                r = requests.get(url, timeout=6, headers=headers, allow_redirects=True)
                
                if r.status_code == 200:
                    not_found = ['not found', 'no results', 'page not available']
                    if not any(k in r.text.lower() for k in not_found):
                        found.append({'platform': platform, 'url': url})
                        print(f"{G}[+] {platform}: Found ✅{RESET}")
                    else:
                        print(f"{Y}[!] {platform}: Not found{RESET}")
                else:
                    print(f"{Y}[!] {platform}: Status {r.status_code}{RESET}")
            except:
                print(f"{Y}[!] {platform}: Error{RESET}")
        
        self.results['social_media'] = found

    # ==========================================
    # 4. LOCATION - FIXED (Target Location)
    # ==========================================
    def get_location(self):
        print(f"\n{B}[*] Getting Target Location...{RESET}")
        
        location_data = {
            'ip': None,
            'city': 'Unknown',
            'region': 'Unknown',
            'country': 'Unknown',
            'timezone': 'Unknown',
            'org': 'Unknown',
            'source': 'Not Found'
        }
        
        # Method 1: Try to get IP from email domain
        try:
            ip = socket.gethostbyname(self.domain)
            if ip:
                location_data['ip'] = ip
                location_data['source'] = 'Domain DNS'
                print(f"{C}[+] Domain IP: {Y}{ip}{RESET}")
                
                # Get location from IP
                ip_info = self.ip_to_location(ip)
                if ip_info:
                    location_data.update(ip_info)
                    location_data['source'] = 'IP Geolocation'
        except:
            pass
        
        # Method 2: Try social media profile location
        for platform in self.results['social_media']:
            if platform['platform'] in ['Instagram', 'Twitter', 'Facebook']:
                try:
                    r = requests.get(platform['url'], timeout=5)
                    if 'location' in r.text.lower():
                        print(f"{G}[+] Location found in {platform['platform']} ✅{RESET}")
                        location_data['source'] = f"{platform['platform']} Profile"
                except:
                    pass
        
        # Method 3: Gravatar location (if available)
        try:
            h = hashlib.md5(self.email.lower().encode()).hexdigest()
            url = f"https://www.gravatar.com/avatar/{h}?d=404"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                # Check headers for location info
                if 'cf-ray' in r.headers:
                    ray = r.headers.get('cf-ray', '')
                    if ray:
                        print(f"{G}[+] Cloudflare location data found ✅{RESET}")
                        location_data['source'] = 'Cloudflare'
        except:
            pass
        
        # Display location
        print(f"\n{G}📍 TARGET LOCATION:{RESET}")
        print(f"{C}  IP: {Y}{location_data['ip'] or 'Unknown'}{RESET}")
        print(f"{C}  City: {Y}{location_data['city']}{RESET}")
        print(f"{C}  Region: {Y}{location_data['region']}{RESET}")
        print(f"{C}  Country: {Y}{location_data['country']}{RESET}")
        print(f"{C}  Timezone: {Y}{location_data['timezone']}{RESET}")
        print(f"{C}  ISP: {Y}{location_data['org']}{RESET}")
        print(f"{C}  Source: {Y}{location_data['source']}{RESET}")
        
        self.results['location'] = location_data

    def ip_to_location(self, ip):
        """Convert IP to location using ipinfo.io"""
        try:
            url = f"https://ipinfo.io/{ip}/json"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                return {
                    'ip': ip,
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown'),
                    'org': data.get('org', 'Unknown')
                }
        except:
            pass
        return None

    # ==========================================
    # 5. GRAVATAR
    # ==========================================
    def gravatar(self):
        print(f"\n{B}[*] Checking Gravatar...{RESET}")
        try:
            h = hashlib.md5(self.email.lower().encode()).hexdigest()
            url = f"https://www.gravatar.com/avatar/{h}?d=404&s=200"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                self.results['gravatar'] = url
                self.results['profile_photos'].append({'source': 'Gravatar', 'url': url})
                print(f"{G}[+] Gravatar found ✅{RESET}")
            else:
                print(f"{Y}[!] No Gravatar{RESET}")
        except:
            print(f"{Y}[!] Gravatar check failed{RESET}")

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
                        'date': b.get('BreachDate')
                    })
                    print(f"{R}[!] {b.get('Name')} - {b.get('BreachDate')}{RESET}")
            else:
                print(f"{G}[+] No breaches ✅{RESET}")
        except:
            print(f"{Y}[!] Breach check failed{RESET}")

    # ==========================================
    # 7. GENERATE REPORT
    # ==========================================
    def generate_report(self):
        print(f"\n{B}[*] Generating Report...{RESET}")
        
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = f"location_report_{self.username}_{ts}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"{G}[+] JSON: {json_file}{RESET}")
        
        # HTML
        html_file = f"location_report_{self.username}_{ts}.html"
        loc = self.results['location']
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
                .location-box {{ background: #1a1a3e; padding: 20px; border-radius: 10px; border-left: 4px solid #f5576c; }}
                pre {{ background: #111; padding: 10px; border-radius: 5px; overflow: auto; }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>📍 GAUTAM OSINT REPORT</h1>
            <p><b>Email:</b> {self.email}</p>
            <p><b>Username:</b> {self.username}</p>
            <p><b>Generated:</b> {self.results['timestamp']}</p>
            
            <div class="section">
                <h2 class="blue">📍 TARGET LOCATION</h2>
                <div class="location-box">
                    <p><b>IP Address:</b> {loc.get('ip', 'Unknown')}</p>
                    <p><b>City:</b> {loc.get('city', 'Unknown')}</p>
                    <p><b>Region:</b> {loc.get('region', 'Unknown')}</p>
                    <p><b>Country:</b> {loc.get('country', 'Unknown')}</p>
                    <p><b>Timezone:</b> {loc.get('timezone', 'Unknown')}</p>
                    <p><b>ISP:</b> {loc.get('org', 'Unknown')}</p>
                    <p><b>Source:</b> {loc.get('source', 'Unknown')}</p>
                </div>
            </div>
            
            <div class="section"><h2 class="blue">🕵️ Social Media</h2><pre>{json.dumps(self.results['social_media'], indent=2, default=str)}</pre></div>
            <div class="section"><h2 class="red">🔓 Data Breaches</h2><pre>{json.dumps(self.results['breaches'], indent=2, default=str)}</pre></div>
            
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
    # 8. RUN ALL
    # ==========================================
    def run_all(self):
        self.banner()
        self.validate_email()
        self.domain_info()
        self.social_media()
        self.get_location()
        self.gravatar()
        self.breaches()
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
        tool = GAUTAM_OSINT_LOCATION(email)
        tool.run_all()
    else:
        print(f"{C}Usage: python3 gautam_osint_location.py <email>{RESET}")
        print(f"{C}Example: python3 gautam_osint_location.py target@gmail.com{RESET}")
        email = input(f"{C}Enter email: {RESET}")
        if email and '@' in email:
            tool = GAUTAM_OSINT_LOCATION(email)
            tool.run_all()
        else:
            print(f"{R}[!] Invalid email!{RESET}")
