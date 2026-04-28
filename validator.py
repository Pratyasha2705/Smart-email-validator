import re
import dns.resolver

def validate_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def get_domain(email):
    return email.split('@')[1]

def check_mx(domain):
   try:
       records = dns.resolver.resolve(domain, 'MX')
       if records:
           return True
       else:
           return False
   except dns.resolver.NoAnswer:
       return False
   except dns.resolver.NXDOMAIN:
       return False
   except Exception as e:
       print("Error:", e)  
       return False
DISPOSABLE_DOMAINS = ["mailinator.com", "10minutemail.com", "tempmail.com"]

def is_disposable(domain):
    return domain in DISPOSABLE_DOMAINS