import requests
import random
import string
import time
import re
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class DeviceFingerprint:
    """Generate realistic Android device fingerprints"""
    
    DEVICES = [
        {"model": "SM-G991B", "name": "Samsung Galaxy S21", "android": "13", "build": "TP1A.220624.014"},
        {"model": "SM-A525F", "name": "Samsung Galaxy A52", "android": "13", "build": "SP1A.210812.016"},
        {"model": "Redmi Note 11", "name": "Redmi Note 11", "android": "12", "build": "SKQ1.211103.001"},
        {"model": "M2101K9G", "name": "Xiaomi 11T", "android": "13", "build": "TKQ1.220829.002"},
        {"model": "CPH2205", "name": "OPPO Reno6", "android": "12", "build": "RKQ1.201217.002"},
        {"model": "RMX3263", "name": "Realme 9 Pro", "android": "12", "build": "RKQ1.211119.001"},
        {"model": "V2111", "name": "Vivo V21", "android": "12", "build": "SP1A.210812.003"},
        {"model": "Pixel 6", "name": "Google Pixel 6", "android": "14", "build": "UP1A.231005.007"},
        {"model": "OnePlus 9", "name": "OnePlus 9", "android": "13", "build": "TP1A.220624.014"},
        {"model": "SM-F711B", "name": "Samsung Galaxy Z Flip 3", "android": "13", "build": "TP1A.220624.014"},
    ]
    
    @staticmethod
    def generate():
        """Generate random device fingerprint"""
        device = random.choice(DeviceFingerprint.DEVICES)
        
        return {
            'device-identifier': device['build'],
            'device-model': device['model'],
            'android-version': device['android'],
            'device-name': device['name']
        }

class RealNameGenerator:
    """Generate realistic names for email"""
    
    FIRST_NAMES = [
        "james", "john", "robert", "michael", "william", "david", "richard", "joseph",
        "thomas", "charles", "daniel", "matthew", "anthony", "donald", "mark", "paul",
        "steven", "andrew", "kenneth", "joshua", "kevin", "brian", "george", "edward",
        "ronald", "timothy", "jason", "jeffrey", "ryan", "jacob", "gary", "nicholas",
        "eric", "jonathan", "stephen", "larry", "justin", "scott", "brandon", "frank",
        "mary", "patricia", "jennifer", "linda", "barbara", "elizabeth", "susan", "jessica",
        "sarah", "karen", "nancy", "lisa", "betty", "margaret", "sandra", "ashley",
        "kimberly", "emily", "donna", "michelle", "carol", "amanda", "melissa", "deborah",
        "stephanie", "rebecca", "sharon", "laura", "cynthia", "kathleen", "amy", "angela",
        "shirley", "anna", "brenda", "pamela", "emma", "nicole", "helen", "samantha"
    ]
    
    LAST_NAMES = [
        "smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis",
        "rodriguez", "martinez", "hernandez", "lopez", "gonzalez", "wilson", "anderson", "thomas",
        "taylor", "moore", "jackson", "martin", "lee", "perez", "thompson", "white",
        "harris", "sanchez", "clark", "ramirez", "lewis", "robinson", "walker", "young",
        "allen", "king", "wright", "scott", "torres", "nguyen", "hill", "flores",
        "green", "adams", "nelson", "baker", "hall", "rivera", "campbell", "mitchell"
    ]
    
    @staticmethod
    def generate_email_username():
        """Generate realistic email username"""
        first = random.choice(RealNameGenerator.FIRST_NAMES)
        last = random.choice(RealNameGenerator.LAST_NAMES)
        
        # Different styles
        styles = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first}_{last}",
            f"{first}{last}{random.randint(10, 99)}",
            f"{first}.{last}{random.randint(1, 9)}",
            f"{first[0]}{last}",
            f"{first}{last[0]}{random.randint(100, 999)}",
        ]
        
        return random.choice(styles)

class BitDoctorAutoRegister:
    def __init__(self, referral_code="V3WJCSP"):
        self.base_url = "https://admin.bitdoctor.ai"
        self.referral_code = referral_code
        self.device = None
        
        self.mail_api = "https://api.mail.tm"
        self.mail_session = requests.Session()
        self.mail_session.timeout = 10
        self.mail_token = None
        
    def get_headers(self):
        """Get headers with current device fingerprint"""
        return {
            'user-agent': 'Dart/3.7 (dart:io)',
            'accept': 'application/json',
            'accept-language': 'en_US',
            'accept-encoding': 'gzip',
            'content-type': 'application/json',
            'device-identifier': self.device['device-identifier'],
            'device-model': self.device['device-model'],
            'platform': 'bit-doctor-android'
        }
    
    def log(self, symbol, message, color=Fore.WHITE):
        """Simple logging with colors"""
        print(f"{color}{symbol} {message}{Style.RESET_ALL}")
    
    def generate_password(self):
        return ''.join(random.choices(string.digits, k=6))
    
    def get_mail_domain(self):
        """Get available Mail.tm domain with retry"""
        for attempt in range(3):
            try:
                response = self.mail_session.get(
                    f"{self.mail_api}/domains",
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    domains = data.get('hydra:member', [])
                    if domains:
                        # Filter active domains
                        active_domains = [d for d in domains if d.get('isActive', False)]
                        if active_domains:
                            return active_domains[0]['domain']
                        elif domains:
                            return domains[0]['domain']
                
                if attempt < 2:
                    time.sleep(2)
                    
            except requests.exceptions.Timeout:
                if attempt < 2:
                    time.sleep(2)
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
        
        return None
    
    def create_temp_email(self):
        """Create temporary email with real name"""
        try:
            # Get domain
            domain = self.get_mail_domain()
            
            if not domain:
                self.log("✗", "Failed to get domain from Mail.tm", Fore.RED)
                return None, None
            
            self.log("✓", f"Domain: {domain}", Fore.GREEN)
            
            # Generate realistic email username
            username = RealNameGenerator.generate_email_username()
            email = f"{username}@{domain}"
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            
            # Create account
            account_data = {
                "address": email,
                "password": password
            }
            
            response = self.mail_session.post(
                f"{self.mail_api}/accounts",
                json=account_data,
                timeout=10
            )
            
            if response.status_code == 201:
                # Get JWT token
                token_response = self.mail_session.post(
                    f"{self.mail_api}/token",
                    json=account_data,
                    timeout=10
                )
                
                if token_response.status_code == 200:
                    token_data = token_response.json()
                    self.mail_token = token_data['token']
                    
                    # Set authorization header
                    self.mail_session.headers.update({
                        'Authorization': f'Bearer {self.mail_token}'
                    })
                    
                    return email, password
                else:
                    self.log("✗", f"Token failed: Status {token_response.status_code}", Fore.RED)
            else:
                self.log("✗", f"Account creation failed: Status {response.status_code}", Fore.RED)
            
            return None, None
            
        except requests.exceptions.Timeout:
            self.log("✗", "Connection timeout", Fore.RED)
            return None, None
        except requests.exceptions.ConnectionError:
            self.log("✗", "Connection error", Fore.RED)
            return None, None
        except Exception as e:
            self.log("✗", f"Error: {str(e)}", Fore.RED)
            return None, None
    
    def get_verification_code(self, max_attempts=25):
        """Get verification code from Mail.tm inbox"""
        print(f"   {Fore.YELLOW}⏳ Waiting for email...{Style.RESET_ALL}", end='\r')
        
        for attempt in range(max_attempts):
            try:
                # Get messages
                response = self.mail_session.get(
                    f"{self.mail_api}/messages",
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    messages = data.get('hydra:member', [])
                    
                    if messages:
                        # Get first message ID
                        message_id = messages[0]['id']
                        
                        # Get full message details
                        msg_response = self.mail_session.get(
                            f"{self.mail_api}/messages/{message_id}",
                            timeout=10
                        )
                        
                        if msg_response.status_code == 200:
                            message = msg_response.json()
                            
                            # Get text content
                            text_content = message.get('text', '')
                            html_content = message.get('html', [])
                            
                            # Combine all content
                            full_content = text_content
                            if isinstance(html_content, list):
                                full_content += ' '.join(html_content)
                            elif isinstance(html_content, str):
                                full_content += html_content
                            
                            # Extract 6-digit code
                            code_match = re.search(r'\b\d{6}\b', full_content)
                            
                            if code_match:
                                return code_match.group(0)
                
                # Show progress
                if attempt < max_attempts - 1:
                    print(f"   {Fore.YELLOW}⏳ Checking inbox... ({attempt + 1}/{max_attempts}){Style.RESET_ALL}", end='\r')
                    time.sleep(3)
                
            except Exception as e:
                if attempt < max_attempts - 1:
                    time.sleep(3)
        
        return None
    
    def register_account(self, email):
        """Register new account"""
        try:
            url = f"{self.base_url}/api/v1/auth/register"
            response = requests.post(
                url, 
                json={"email": email}, 
                headers=self.get_headers(),
                timeout=15
            )
            result = response.json()
            
            if result.get('success'):
                return result['data']['user_id']
            else:
                self.log("✗", f"Register failed: {result.get('message')}", Fore.RED)
                return None
                
        except Exception as e:
            self.log("✗", f"Register error: {str(e)}", Fore.RED)
            return None
    
    def verify_email(self, email, pin_code):
        """Verify email with OTP"""
        try:
            url = f"{self.base_url}/api/v1/auth/verify-email"
            data = {"email": email, "pin_code": pin_code}
            response = requests.post(
                url, 
                json=data, 
                headers=self.get_headers(),
                timeout=15
            )
            result = response.json()
            
            return result.get('success', False)
                
        except Exception as e:
            self.log("✗", f"Verify error: {str(e)}", Fore.RED)
            return False
    
    def set_password(self, email, password):
        """Set account password"""
        try:
            url = f"{self.base_url}/api/v1/auth/set-password"
            data = {
                "email": email,
                "password": password,
                "password_confirmation": password
            }
            response = requests.post(
                url, 
                json=data, 
                headers=self.get_headers(),
                timeout=15
            )
            result = response.json()
            
            return result.get('success', False)
                
        except Exception as e:
            self.log("✗", f"Password error: {str(e)}", Fore.RED)
            return False
    
    def verify_referral(self, email):
        """Apply referral code"""
        try:
            url = f"{self.base_url}/api/v1/referral/verify-code"
            data = {"referral_code": self.referral_code, "email": email}
            response = requests.post(
                url, 
                json=data, 
                headers=self.get_headers(),
                timeout=15
            )
            result = response.json()
            
            return result.get('success', False)
                
        except Exception as e:
            return False
    
    def auto_register(self):
        """Main registration flow"""
        print(f"\n{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        # Generate unique device fingerprint
        self.device = DeviceFingerprint.generate()
        self.log("●", f"Device: {self.device['device-name']}", Fore.CYAN)
        
        # Step 1: Create temp email with real name
        self.log("●", "Creating email with real name...", Fore.YELLOW)
        email, _ = self.create_temp_email()
        
        if not email:
            self.log("✗", "Failed to create email", Fore.RED)
            return None
        
        self.log("✓", f"Email: {email}", Fore.GREEN)
        time.sleep(2)
        
        # Step 2: Register account
        self.log("●", "Registering account...", Fore.YELLOW)
        user_id = self.register_account(email)
        
        if not user_id:
            return None
        
        self.log("✓", "Registered", Fore.GREEN)
        time.sleep(3)
        
        # Step 3: Get verification code
        self.log("●", "Getting verification code...", Fore.YELLOW)
        pin_code = self.get_verification_code()
        
        if not pin_code:
            self.log("✗", "No code received" + " " * 20, Fore.RED)
            return None
        
        print(f"   {Fore.YELLOW}⏳ Checking inbox... ({25}/{25}){Style.RESET_ALL}", end='\r')
        self.log("✓", f"Code: {pin_code}" + " " * 30, Fore.GREEN)
        time.sleep(1)
        
        # Step 4: Verify email
        self.log("●", "Verifying email...", Fore.YELLOW)
        if not self.verify_email(email, pin_code):
            self.log("✗", "Verification failed", Fore.RED)
            return None
        
        self.log("✓", "Email verified", Fore.GREEN)
        time.sleep(1)
        
        # Step 5: Set password
        password = self.generate_password()
        self.log("●", "Setting password...", Fore.YELLOW)
        
        if not self.set_password(email, password):
            self.log("✗", "Password failed", Fore.RED)
            return None
        
        self.log("✓", f"Password: {password}", Fore.GREEN)
        time.sleep(1)
        
        # Step 6: Apply referral
        self.log("●", "Applying referral...", Fore.YELLOW)
        self.verify_referral(email)
        self.log("✓", f"Referral: {self.referral_code}", Fore.GREEN)
        
        # Account info
        account_info = {
            'email': email,
            'password': password,
            'user_id': user_id,
            'referral_code': self.referral_code,
            'device': self.device['device-name'],
            'device_model': self.device['device-model']
        }
        
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ SUCCESS{Style.RESET_ALL}\n")
        
        return account_info

def print_banner():
    banner = f"""
{Fore.CYAN}╔{'═' * 48}╗
║{' ' * 5}Bitdoctor Auto Register - BY GIEMDFK{' ' * 8}║
╚{'═' * 48}╝{Style.RESET_ALL}
"""
    print(banner)

def main():
    print_banner()
    
    # Input
    ref_input = input(f"{Fore.YELLOW}Referral Code (default: V3WJCSP): {Style.RESET_ALL}").strip()
    referral_code = ref_input if ref_input else "V3WJCSP"
    
    try:
        num_accounts = int(input(f"{Fore.YELLOW}Number of accounts: {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}Invalid number, using 1{Style.RESET_ALL}")
        num_accounts = 1
    
    # Initialize bot
    bot = BitDoctorAutoRegister(referral_code=referral_code)
    results = []
    
    # Create accounts
    for i in range(num_accounts):
        print(f"\n{Fore.MAGENTA}━━━ Account {i+1}/{num_accounts} ━━━{Style.RESET_ALL}")
        
        result = bot.auto_register()
        
        if result:
            results.append(result)
            
            # Save to file with device info
            with open('bitdoctor_accounts.txt', 'a', encoding='utf-8') as f:
                f.write(f"{result['email']}|{result['password']}|{result['user_id']}|{result['device']}|{result['device_model']}\n")
        
        # Delay between accounts
        if i < num_accounts - 1:
            delay = random.randint(5, 10)
            print(f"\n{Fore.YELLOW}⏳ Next in {delay}s...{Style.RESET_ALL}")
            time.sleep(delay)
    
    # Final summary
    print(f"\n{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
    print(f"Total    : {num_accounts}")
    print(f"Success  : {Fore.GREEN}{len(results)}{Style.RESET_ALL}")
    print(f"Failed   : {Fore.RED}{num_accounts - len(results)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}\n")
    
    if results:
        print(f"{Fore.GREEN}✓ Saved: bitdoctor_accounts.txt{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Format: email|password|user_id|device|model{Style.RESET_ALL}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}✗ Stopped{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}\n")
