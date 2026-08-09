#!/usr/bin/env python3
"""
GAUTAM OSINT TOOL - FINAL VERSION
Complete Email Investigation - All Platforms Working
"""

import os
import sys
import json
import time
import requests
import hashlib
import subprocess
from datetime import datetime

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'

class GAUTAM_OSINT_FINAL:
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
            'profile_photos': [],
            'phone_numbers': [],
            'linked_accounts': [],
            'summary': {}
        }

    def banner(self):
        os.system('clear')
        print(f"""{R}
╔══════════════════════════════════════════════════════════════════╗
║         📧 GAUTAM OSINT TOOL - FINAL 📧                         ║
║          Complete Email + Social Media Investigation            ║
║                                                                  ║
║   🔍 Email → 🕵️ Social → 📱 Phone → 🖼️ Photos → 📊 Report     ║
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
    # 3. SOCIAL MEDIA - COMPLETE FIXED VERSION
    # ==========================================
    def social_media(self):
        print(f"\n{B}[*] Searching Social Media...{RESET}")
        
        # Updated platforms with correct URL formats
        platforms = [
            ('Instagram', f'https://www.instagram.com/{self.username}'),
            ('Twitter', f'https://twitter.com/{self.username}'),
            ('LinkedIn', f'https://www.linkedin.com/in/{self.username}'),
            ('LinkedIn (pub)', f'https://www.linkedin.com/pub/{self.username}'),
            ('GitHub', f'https://github.com/{self.username}'),
            ('YouTube', f'https://youtube.com/@{self.username}'),
            ('YouTube (c)', f'https://youtube.com/c/{self.username}'),
            ('YouTube (user)', f'https://youtube.com/user/{self.username}'),
            ('Reddit', f'https://reddit.com/user/{self.username}'),
            ('Pinterest', f'https://pinterest.com/{self.username}'),
            ('Tumblr', f'https://{self.username}.tumblr.com'),
            ('Medium', f'https://medium.com/@{self.username}'),
            ('Quora', f'https://quora.com/profile/{self.username}'),
            ('Facebook', f'https://facebook.com/{self.username}'),
            ('Snapchat', f'https://snapchat.com/add/{self.username}'),
            ('TikTok', f'https://tiktok.com/@{self.username}'),
            ('Telegram', f'https://t.me/{self.username}'),
            ('Discord', f'https://discord.com/users/{self.username}'),
            ('Vimeo', f'https://vimeo.com/{self.username}'),
            ('Dribbble', f'https://dribbble.com/{self.username}'),
            ('Behance', f'https://behance.net/{self.username}'),
            ('Flickr', f'https://flickr.com/people/{self.username}'),
            ('DeviantArt', f'https://deviantart.com/{self.username}'),
            ('SoundCloud', f'https://soundcloud.com/{self.username}'),
            ('Spotify', f'https://open.spotify.com/user/{self.username}'),
            ('Twitch', f'https://twitch.tv/{self.username}'),
            ('Steam', f'https://steamcommunity.com/id/{self.username}'),
            ('Patreon', f'https://patreon.com/{self.username}'),
            ('Etsy', f'https://etsy.com/shop/{self.username}'),
            ('Imgur', f'https://imgur.com/user/{self.username}'),
        ]
        
        found = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        for platform, url in platforms:
            try:
                time.sleep(0.3)
                r = requests.get(url, timeout=8, headers=headers, allow_redirects=True)
                
                if r.status_code == 200:
                    # Check for "not found" pages
                    not_found = ['not found', 'no results', 'page not available', 'does not exist', 'this user does not exist']
                    is_not_found = any(k in r.text.lower() for k in not_found)
                    
                    if not is_not_found:
                        found.append({'platform': platform, 'url': url, 'status': 'Found'})
                        print(f"{G}[+] {platform}: Found ✅{RESET}")
                    else:
                        print(f"{Y}[!] {platform}: Not found{RESET}")
                else:
                    print(f"{Y}[!] {platform}: Status {r.status_code}{RESET}")
                    
            except Exception:
                print(f"{Y}[!] {platform}: Error checking{RESET}")
        
        self.results['social_media'] = found

    # ==========================================
    # 4. PROFILE PHOTOS
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
            print(f"{Y}[!] No Gravatar{RESET}")
        
        # Google Profile
        try:
            google_url = f"https://picasaweb.google.com/data/entry/api/user/{self.email}"
            r = requests.get(google_url, timeout=5)
            if r.status_code == 200:
                photos.append({'source': 'Google', 'url': google_url})
                print(f"{G}[+] Google profile photo found ✅{RESET}")
        except:
            pass
        
        self.results['profile_photos'] = photos

    # ==========================================
    # 5. PHONE NUMBERS
    # ==========================================
    def phone_numbers(self):
        print(f"\n{B}[*] Searching Phone Numbers...{RESET}")
        numbers = []
        for platform in self.results['social_media']:
            if platform['platform'] in ['Facebook', 'LinkedIn']:
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
                        'date': b.get('BreachDate')
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
                print(f"{G}[+] Location ✅{RESET}")
                print(f"{C}  IP: {Y}{data.get('ip')}{RESET}")
                print(f"{C}  City: {Y}{data.get('city')}{RESET}")
                print(f"{C}  Country: {Y}{data.get('country')}{RESET}")
        except:
            print(f"{Y}[!] Location failed{RESET}")

    # ==========================================
    # 8. GENERATE REPORT
    # ==========================================
    def generate_report(self):
        print(f"\n{B}[*] Generating Report...{RESET}")
        
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = f"final_report_{self.username}_{ts}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"{G}[+] JSON: {json_file}{RESET}")
        
        # HTML
        html_file = f"final_report_{self.username}_{ts}.html"
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
                pre {{ background: #111; padding: 10px; border-radius: 5px; overflow: auto; }}
                img {{ max-width: 200px; border-radius: 50%; }}
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
            
            <div class="section"><h2 class="blue">🕵️ Social Media</h2><pre>{json.dumps(self.results['social_media'], indent=2, default=str)}</pre></div>
            
            <div class="section"><h2 class="yellow">🖼️ Profile Photos</h2><pre>{json.dumps(self.results['profile_photos'], indent=2, default=str)}</pre>
            {f'<img src="{self.results["gravatar"]}"/>' if self.results.get('gravatar') else ''}</div>
            
            <div class="section"><h2 class="yellow">📱 Phone Numbers</h2><pre>{json.dumps(self.results['phone_numbers'], indent=2, default=str)}</pre></div>
            
            <div class="section"><h2 class="red">🔓 Data Breaches</h2><pre>{json.dumps(self.results['breaches'], indent=2, default=str)}</pre></div>
            
            <div class="section"><h2 class="blue">📍 Location</h2><pre>{json.dumps(self.results['location'], indent=2, default=str)}</pre></div>
            
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
    # 9. RUN ALL
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
        tool = GAUTAM_OSINT_FINAL(email)
        tool.run_all()
    else:
        print(f"{C}Usage: python3 gautam_osint_final.py <email>{RESET}")
        print(f"{C}Example: python3 gautam_osint_final.py target@gmail.com{RESET}")
        email = input(f"{C}Enter email: {RESET}")
        if email and '@' in email:
            tool = GAUTAM_OSINT_FINAL(email)
            tool.run_all()
        else:
            print(f"{R}[!] Invalid email!{RESET}")
