from pathlib import Path
import re, logging, requests, time, os

MAX_ATTEMPTS = 5
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def extract_ip(line):
    pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    match = pattern.search(line)
    if match != None:
        return match.group()
    else:
        return None

def send_alert(found_ip, ip_count, URL):
    payload = {}
    message = f"ALERT: Force brute détéctée depuis l'{found_ip} ({ip_count} tentatives)'"
    payload['content'] = message
    requests.post(URL, json=payload)
    
def main():
    auth_file = open(Path.home() / 'auth.log', 'r')
    ip_counts = {}

    while True:
        line = auth_file.readline()
        if line == "":
            time.sleep(1)
            continue

        if 'Failed password' in line:
            found_ip = extract_ip(line)
            if found_ip != None:
                if found_ip not in ip_counts:
                    ip_counts[found_ip] = 1
                else:
                    ip_counts[found_ip] += 1

                if ip_counts[found_ip] >= MAX_ATTEMPTS:
                    #print(f"ALERT: Force brute détéctée depuis l'{found_ip} ({ip_counts[found_ip]} tentatives)'")
                    send_alert(found_ip, ip_counts[found_ip], URL=WEBHOOK_URL)
            else:
                continue


if __name__ == '__main__':
    main()
