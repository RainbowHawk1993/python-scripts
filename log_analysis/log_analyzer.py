import re
import sys
from collections import Counter

LOG_PATTERN = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[.*\] "(?P<method>[A-Z]+) (?P<url>.+?) HTTP/[\d\.]+" (?P<status>\d{3}) (?P<size>\d+)'

def analyze_log(file_path):
    ip_counter = Counter()
    error_counter = Counter()
    total_size = 0
    total_requests = 0

    with open(file_path, 'r') as log_file:
        for line in log_file:
            match = re.match(LOG_PATTERN, line)
            if match:
                ip = match.group('ip')
                status = match.group('status')
                size = int(match.group('size'))
                ip_counter[ip] += 1

                if status.startswith(('4', '5')):
                    error_counter[status] += 1

                total_size += size
                total_requests += 1

    top_ips = ip_counter.most_common(5)
    most_frequent_errors = error_counter.most_common()
    average_size = total_size / total_requests if total_requests > 0 else 0

    print("Top 5 IP addresses with the most requests:")
    for ip, count in top_ips:
        print(f"{ip}: {count} requests")

    print("\nMost frequent errors (4xx and 5xx):")
    for error, count in most_frequent_errors:
        print(f"HTTP {error}: {count} occurrences")

    print(f"\nAverage response size: {average_size:.2f} bytes")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <log_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    analyze_log(log_file_path)
