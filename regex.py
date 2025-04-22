#regular expressions in python
# + represent one or more occurrences of the preceding character or group.
# a+ matches "a", "aa", "aaa", and so on.

#/w matches any word character (alphanumeric and underscore).
#/w+ matches one or more word characters.

#/d matches any digit.
#/d+ matches one or more digits.

#/s matches any whitespace character (space, tab, newline).
#/s+ matches one or more whitespace characters.

#/b matches a word boundary.
#/bword\b matches "word" as a whole word.   

#regular expressions in python
# + represent one or more occurrences of the preceding character or group.
# a+ matches "a", "aa", "aaa", and so on.

import re

# Collection of regex patterns with examples
regex_examples = {
    # IP address matching (IPv4)
    "ipv4": {
        "pattern": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "examples": ["192.168.1.1", "10.0.0.1", "172.16.254.1"],
        "description": "Matches IPv4 addresses (simple pattern, doesn't validate ranges)"
    },
    
    # More accurate IPv4 validation
    "ipv4_strict": {
        "pattern": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
        "examples": ["192.168.1.1", "255.255.255.255", "0.0.0.0"],
        "description": "Validates IPv4 addresses with proper range checking"
    },
    
    # MAC address matching
    "mac_address": {
        "pattern": r"(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}",
        "examples": ["00:1A:2B:3C:4D:5E", "00-1A-2B-3C-4D-5E"],
        "description": "Matches MAC addresses with : or - separators"
    },
    
    # Email address matching
    "email": {
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "examples": ["user@example.com", "john.doe123@company-name.co.uk"],
        "description": "Matches email addresses"
    },
    
    # URL matching
    "url": {
        "pattern": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
        "examples": ["https://www.example.com", "http://subdomain.example.co.uk/path?query=value"],
        "description": "Matches HTTP and HTTPS URLs"
    },
    
    # Credit card number (simplified)
    "credit_card": {
        "pattern": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
        "examples": ["1234-5678-9012-3456", "1234 5678 9012 3456", "1234567890123456"],
        "description": "Matches credit card numbers with or without separators"
    },
    
    # Password strength check (minimum 8 chars, at least one uppercase, lowercase, number, and special char)
    "strong_password": {
        "pattern": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        "examples": ["Passw0rd!", "Str0ng@Pass"],
        "description": "Validates strong passwords with specific requirements"
    },
    
    # Date formats (MM/DD/YYYY or DD/MM/YYYY)
    "date": {
        "pattern": r"\b(?:0[1-9]|[12][0-9]|3[01])[/.-](?:0[1-9]|1[0-2])[/.-](?:19|20)\d\d\b",
        "examples": ["25/12/2023", "01-31-2022", "12.25.2021"],
        "description": "Matches dates in various formats"
    },
    
    # Log file timestamp
    "log_timestamp": {
        "pattern": r"\b\d{4}[-/]\d{2}[-/]\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b",
        "examples": ["2023-09-15T13:45:30Z", "2023/09/15 13:45:30.123+01:00"],
        "description": "Matches ISO 8601 and common log timestamps"
    },
    
    # Windows file path
    "windows_path": {
        "pattern": r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*",
        "examples": ["C:\\Users\\Username\\Documents\\file.txt", "D:\\Program Files\\App\\"],
        "description": "Matches Windows file paths"
    },
    
    # Linux/Unix file path
    "unix_path": {
        "pattern": r"/(?:[^/\0]+/)*[^/\0]*",
        "examples": ["/etc/passwd", "/var/log/syslog", "/home/user/documents/file.txt"],
        "description": "Matches Unix/Linux file paths"
    },
    
    # Domain name
    "domain": {
        "pattern": r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}",
        "examples": ["example.com", "sub.domain.co.uk"],
        "description": "Matches domain names"
    },
    
    # UUID/GUID
    "uuid": {
        "pattern": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        "examples": ["550e8400-e29b-41d4-a716-446655440000", "123e4567-e89b-12d3-a456-426614174000"],
        "description": "Matches UUIDs/GUIDs"
    }
}

# Example of using these patterns
def test_regex_pattern(pattern_name):
    pattern_info = regex_examples.get(pattern_name)
    if not pattern_info:
        print(f"Pattern '{pattern_name}' not found")
        return
    
    print(f"Testing pattern: {pattern_name}")
    print(f"Description: {pattern_info['description']}")
    print(f"Regex pattern: {pattern_info['pattern']}")
    
    pattern = re.compile(pattern_info['pattern'])
    
    print("\nMatching examples:")
    for example in pattern_info['examples']:
        match = pattern.search(example)
        print(f"  '{example}': {'✓ Match' if match else '✗ No match'}")
    
    print("\n")

# Test a few patterns
test_regex_pattern("ipv4")
test_regex_pattern("email")
test_regex_pattern("mac_address")

# Device IDs for practice
device_Ids = [
    "192.168.1.100",                          # IP address
    "00:1A:2B:3C:4D:5E",                      # MAC address
    "server-rack01-unit05",                   # Server identifier
    "fw-edge-01",                             # Firewall identifier
    "550e8400-e29b-41d4-a716-446655440000",   # UUID
    "SN-2023-45678-ABCD",                     # Serial number
    "admin@network.local",                    # Email
    "C:\\Devices\\Inventory\\switches.csv",   # Windows path
    "/var/log/devices/routers.log",           # Unix path
    "https://device-portal.company.com"       # URL
]

# Example: Find all MAC addresses in the device_Ids list
def find_mac_addresses():
    mac_pattern = re.compile(regex_examples["mac_address"]["pattern"])
    matches = [device for device in device_Ids if mac_pattern.search(device)]
    print(f"Found {len(matches)} MAC addresses:")
    for match in matches:
        print(f"  - {match}")

# Example: Extract all IPs from a log file content
sample_log = """
2023-09-15T13:45:30Z Connection from 192.168.1.100 to server at 10.0.0.1
2023-09-15T13:46:12Z Failed login attempt from 172.16.254.1
2023-09-15T13:47:05Z Device 00:1A:2B:3C:4D:5E connected to network
"""

def extract_ips_from_log():
    ip_pattern = re.compile(regex_examples["ipv4"]["pattern"])
    matches = ip_pattern.findall(sample_log)
    print(f"Found {len(matches)} IP addresses in log:")
    for match in matches:
        print(f"  - {match}")

# Run the examples
print("===== REGEX EXAMPLES FOR CYBERSECURITY =====\n")
find_mac_addresses()
print()
extract_ips_from_log()