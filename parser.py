import argparse
from utils import count_failed_login_ips

# Define output location.
OUTPUT_LOC = 'output/top_ips.txt'

def show_top_ips(ip_counts, top_n=5):
    
    sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"\n🔐 Top {top_n} Failed SSH Login IPs:\n")
    for ip, count in sorted_ips[:top_n]:
        print*(f"{ip} - {count} attempts")

    return sorted_ips[:top_n]
def save_to_file(ip_list, path=OUTPUT_LOC):
    
    try:
        with open(path, 'w') as f:
            for ip, count in ip_list:
                f.write(f"{ip} - {count} attempts\n")
        print(f"\n✅ Results saved to {path}")
    except Exception as e:
        print(f"[!] Failed to save file {e}")

def main():
    parser = argparse.ArgumentParser(description="SSH Failed Login Parser leverageing systemd journal logging")
    parser.add_argument("--top", type=int, default=5, help="Number of top offending IP addressees to display")
    parser.add_argument("--save", action="store_true", help="Save resultes to output folder in top_ips.txt")

    args = parser.parse_args()

    ip_counts = count_failed_login_ips()

    if not ip_counts:
        print("[!] No Failed SSH login attempts found!")
        return
    top_ips = show_top_ips(ip_counts, top_n=args.top)

    if args.save:
        save_to_file(top_ips)


if __name__ == "__main__":
    main()