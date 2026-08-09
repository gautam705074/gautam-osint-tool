#!/usr/bin/env python3
"""
GAUTAM OSINT TOOL - TARGET LOCATION FINDER
Real Target Location from Email, Headers, Links
"""

import os
import sys
import json
import time
import requests
import hashlib
import socket
import dns.resolver
import re
from datetime import datetime
import subprocess

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'

class TARGET_LOCATION_FINDER:
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
            'location': {
                'ip': None,
                'city': 'Unknown',
                'region': 'Unknown',
                'country': 'Unknown',
                'timezone': 'Unknown',
                'org': 'Unknown',
                'source': 'Not Found'
            },
            'email_header_ip': None,
            'social_location': [],
            'breaches': [],
            'gravatar': None,
            'summary': {}
        }

    def banner(self):
        os.system('clear')
        print(f"""{R}
╔══════════════════════════════════════════════════════════════════╗
║         📧 GAUTAM TARGET LOCATION FINDER 📧                     ║
║          Real Location from Email / Headers / Links             ║
║                                                                  ║
║   📧 Email → 📍 Location → 🕵️ Social → 📊 Report              ║
╚══════════════════════════════════════════════════════════════════╝{RESET}
""")
        print(f"{C}[+] Target: {Y}{self.email}{RESET}")
        print(f"{C}[+] Username: {Y}{self.username}{RESET}")
        print("="*70)

    # ==========================================
    # METHOD 1: EMAIL VALIDATION
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
    # METHOD 2: GET LOCATION FROM EMAIL HEADER
    # ==========================================
    def location_from_header(self):
        print(f"\n{B}[*] Method 1: Checking Email Headers...{RESET}")
        
        # Instructions for user
        print(f"{Y}[!] To get location from email header:{RESET}")
        print(f"{C}  1. Open email in Gmail/Outlook{RESET}")
        print(f"{C}  2. Click 'Show original' / 'View Source'{RESET}")
        print(f"{C}  3. Find 'Received: from' IP addresses{RESET}")
        print(f"{C}  4. Copy the IP and paste below{RESET}")
        
        # Ask for manual IP input
        print(f"\n{C}Would you like to: {RESET}")
        print(f"{G}  a) Enter IP manually from email header{RESET}")
        print(f"{Y}  b) Auto-detect from domain{RESET}")
        print(f"{R}  c) Skip (no email header available){RESET}")
        
        choice = input(f"{C}Enter choice (a/b/c): {RESET}").lower()
        
        if choice == 'a':
            ip = input(f"{C}Enter IP from email header: {RESET}")
            if ip:
                self.get_location_from_ip(ip, 'Email Header')
        
        elif choice == 'b':
            # Auto-detect from domain
            try:
                ip = socket.gethostbyname(self.domain)
                if ip:
                    print(f"{C}[+] Domain IP: {Y}{ip}{RESET}")
                    self.get_location_from_ip(ip, 'Domain DNS')
            except:
                print(f"{R}[!] Could not resolve domain{RESET}")
        
        else:
            print(f"{Y}[!] Skipping email header method{RESET}")

    # ==========================================
    # METHOD 3: LOCATION FROM IP
    # ==========================================
    def get_location_from_ip(self, ip, source):
        """Get location from IP address using ipinfo.io"""
        print(f"\n{B}[*] Getting location for IP: {Y}{ip}{RESET}")
        
        try:
            url = f"https://ipinfo.io/{ip}/json"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                data = r.json()
                self.results['location'] = {
                    'ip': ip,
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                    'source': source
                }
                self.results['email_header_ip'] = ip
                
                # Display location
                print(f"\n{G}📍 TARGET LOCATION FOUND!{RESET}")
                print(f"{C}  IP: {Y}{ip}{RESET}")
                print(f"{C}  City: {Y}{self.results['location']['city']}{RESET}")
                print(f"{C}  Region: {Y}{self.results['location']['region']}{RESET}")
                print(f"{C}  Country: {Y}{self.results['location']['country']}{RESET}")
                print(f"{C}  Timezone: {Y}{self.results['location']['timezone']}{RESET}")
                print(f"{C}  ISP: {Y}{self.results['location']['org']}{RESET}")
                print(f"{C}  Source: {Y}{source}{RESET}")
                return True
            else:
                print(f"{R}[!] Location not found{RESET}")
        except Exception as e:
            print(f"{R}[!] Error: {e}{RESET}")
        return False

    # ==========================================
    # METHOD 4: LOCATION FROM SOCIAL MEDIA
    # ==========================================
    def location_from_social(self):
        print(f"\n{B}[*] Method 2: Checking Social Media...{RESET}")
        
        platforms = [
            ('Instagram', f'https://www.instagram.com/{self.username}'),
            ('Twitter', f'https://twitter.com/{self.username}'),
            ('Facebook', f'https://facebook.com/{self.username}'),
            ('LinkedIn', f'https://linkedin.com/in/{self.username}'),
            ('YouTube', f'https://youtube.com/@{self.username}'),
        ]
        
        found_location = False
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        for platform, url in platforms:
            try:
                r = requests.get(url, timeout=5, headers=headers)
                
                if r.status_code == 200:
                    # Search for location keywords
                    location_keywords = ['location', 'city', 'country', 'delhi', 'mumbai', 'new york', 'london']
                    found = [kw for kw in location_keywords if kw in r.text.lower()]
                    
                    if found:
                        print(f"{G}[+] {platform}: Possible location found ✅{RESET}")
                        self.results['social_location'].append({
                            'platform': platform,
                            'url': url,
                            'keywords': found
                        })
                        found_location = True
                    else:
                        print(f"{Y}[!] {platform}: No location found{RESET}")
                else:
                    print(f"{Y}[!] {platform}: Not accessible{RESET}")
            except:
                print(f"{Y}[!] {platform}: Error checking{RESET}")
        
        if not found_location:
            print(f"{Y}[!] No location found on social media{RESET}")
            print(f"{C}  Tip: Check profile bio for location{RESET}")

    # ==========================================
    # METHOD 5: GRABIFY LINK GENERATOR
    # ==========================================
    def generate_grabify_link(self):
        print(f"\n{B}[*] Method 3: Grabify Link Generator...{RESET}")
        
        print(f"{Y}[!] Grabify tracks IP when link is clicked{RESET}")
        print(f"{C}  1. Go to: https://grabify.link{RESET}")
        print(f"{C}  2. Enter any URL (like google.com){RESET}")
        print(f"{C}  3. Copy the generated link{RESET}")
        print(f"{C}  4. Send it to target via email{RESET}")
        print(f"{C}  5. Check dashboard for IP and location{RESET}")
        
        print(f"\n{Y}[!] Alternative - Use IP logger:{RESET}")
        print(f"{C}  1. Go to: https://iplogger.org{RESET}")
        print(f"{C}  2. Generate tracking link{RESET}")
        print(f"{C}  3. Send to target{RESET}")
        print(f"{C}  4. Check IP and location when clicked{RESET}")
        
        self.results['summary']['grabify'] = {
            'status': 'Manual process',
            'instructions': 'Visit grabify.link to create tracking link'
        }

    # ==========================================
    # METHOD 6: GRAVATAR LOCATION
    # ==========================================
    def gravatar_location(self):
        print(f"\n{B}[*] Checking Gravatar...{RESET}")
        try:
            h = hashlib.md5(self.email.lower().encode()).hexdigest()
            url = f"https://www.gravatar.com/avatar/{h}?d=404&s=200"
            r = requests.get(url, timeout=5)
            
            if r.status_code == 200:
                self.results['gravatar'] = url
                print(f"{G}[+] Gravatar found ✅{RESET}")
                
                # Check headers for location info
                if 'cf-ray' in r.headers:
                    print(f"{C}  Cloudflare region info available{RESET}")
            else:
                print(f"{Y}[!] No Gravatar{RESET}")
        except:
            print(f"{Y}[!] Gravatar check failed{RESET}")

    # ==========================================
    # METHOD 7: DATA BREACHES
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
    # GENERATE REPORT
    # ==========================================
    def generate_report(self):
        print(f"\n{B}[*] Generating Report...{RESET}")
        
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = f"target_location_{self.username}_{ts}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"{G}[+] JSON: {json_file}{RESET}")
        
        # HTML
        html_file = f"target_location_{self.username}_{ts}.html"
        loc = self.results['location']
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Target Location - {self.email}</title>
            <style>
                body {{ font-family: Arial; background: #0a0a0a; color: #fff; padding: 20px; }}
                .container {{ max-width: 900px; margin: auto; background: #1a1a2e; padding: 20px; border-radius: 10px; }}
                h1 {{ color: #f5576c; text-align: center; }}
                .section {{ background: #2a2a3e; padding: 15px; margin: 10px 0; border-radius: 8px; }}
                .location-box {{ background: #1a1a3e; padding: 20px; border-radius: 10px; border-left: 4px solid #f5576c; }}
                .green {{ color: #2ecc71; }}
                .red {{ color: #e74c3c; }}
                .yellow {{ color: #f1c40f; }}
                .blue {{ color: #3498db; }}
                pre {{ background: #111; padding: 10px; border-radius: 5px; overflow: auto; }}
                .instruction {{ background: #2a2a4e; padding: 15px; border-radius: 8px; border-left: 4px solid #f1c40f; }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>📍 TARGET LOCATION REPORT</h1>
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
            
            <div class="section">
                <h2 class="yellow">📧 How to Find Target Location</h2>
                <div class="instruction">
                    <p><b>Method 1: Email Header</b></p>
                    <p>1. Open email → Click "Show original"</p>
                    <p>2. Find "Received: from" → Copy IP</p>
                    <p>3. Use: curl https://ipinfo.io/IP</p>
                    <br>
                    <p><b>Method 2: Grabify Link</b></p>
                    <p>1. Go to grabify.link</p>
                    <p>2. Create tracking link</p>
                    <p>3. Send to target via email</p>
                    <p>4. Check dashboard for location</p>
                </div>
            </div>
            
            <div class="section"><h2 class="blue">🕵️ Social Media</h2><pre>{json.dumps(self.results['social_location'], indent=2, default=str)}</pre></div>
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
    # RUN ALL METHODS
    # ==========================================
    def run_all(self):
        self.banner()
        self.validate_email()
        
        print(f"\n{C}═══════════════════════════════════════════════════════════════{RESET}")
        print(f"{B}📍 FINDING TARGET LOCATION - 3 METHODS{RESET}")
        print(f"{C}═══════════════════════════════════════════════════════════════{RESET}")
        
        # Method 1: Email Header
        self.location_from_header()
        
        # Method 2: Social Media
        self.location_from_social()
        
        # Method 3: Grabify
        self.generate_grabify_link()
        
        # Extra
        self.gravatar_location()
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
        tool = TARGET_LOCATION_FINDER(email)
        tool.run_all()
    else:
        print(f"{C}Usage: python3 gautam_osint_target_location.py <email>{RESET}")
        print(f"{C}Example: python3 gautam_osint_target_location.py target@gmail.com{RESET}")
        email = input(f"{C}Enter email: {RESET}")
        if email and '@' in email:
            tool = TARGET_LOCATION_FINDER(email)
            tool.run_all()
        else:
            print(f"{R}[!] Invalid email!{RESET}")
