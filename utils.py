import re
from collections import defaultdict
from systemd import journal

# Define Regex Pattern matching failed SSH login IP addresses
FAILED_SSH_PATTERN = re.compile(
    r"Failed password for \S+ from (\d{1,3}\.){3}\d{1,3} port \d+ \S+"
)

# Define function that takes an argument and uses the regex pattern to obtain string and extract ip address out of it. 
def extract_log_ip(log):
    
    # Match regex pattern.
    match = FAILED_SSH_PATTERN.search(log)

    # If matched return ip address, if not return nothing. 
    if match:
        return match.group(1)
    return None

# Define function that counts all of the failed login attempts. 
def count_failed_login_ips():
    ip_counts = defaultdict(int)
    
    try:
        journalctl = journal.Reader()
        journalctl.log_level(journal.LOG_INFO)
        journalctl.add_match(_SYSTEMD_UNIT="sshd.service")
        journalctl.seek_tail()
        journalctl.get_previous(10000) #Can be adjusted to add more history of logs.
        journalctl.seek_head()

        for entry in journalctl:
            log = entry.get("MESSAGE", "")
            ip = extract_log_ip(log)
            if ip:
                ip_counts[ip] += 1

    except Exception as e:
        print(f"[!] Error reading journal: {e}")


    return dict(ip_counts)
