from pathlib import Path     # Import the Path module to open the test file and read it
import re, logging, requests, time, os       # Import necessary modules: regex, requests (payload to discord), time (wait time to not overload system), os (environment variables)

MAX_ATTEMPTS = 5         # The maximum attempts to trigger the alert
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")         # URL is securely stored via systemctl environment variable

# Function to extract the IP of the attacker
def extract_ip(line):
    pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    match = pattern.search(line)
    if match != None:
        return match.group()
    else:
        return None

# Function to craft and post the alert to Discord server
def send_alert(found_ip, ip_count, URL):
    payload = {}
    message = f"ALERT: Force brute détéctée depuis l'{found_ip} ({ip_count} tentatives)"
    payload['content'] = message
    requests.post(URL, json=payload)
    
# The main function which contains the logic of the program
def main():
    auth_file = open(Path.home() / 'auth.log', 'r')   # Open the test auth.log in read mode
    ip_counts = {}  # Declare the dictionary which will contain the attackers IPs and their count

    while True:             # This while loop makes the program act like a daemon and run continuously in the background
                            
        line = auth_file.readline()      # A method which reads the auth.log file line by line
        
        if line == "":                   # If we have an empty line (EOF), wait 1 second and return
            time.sleep(1)                # to the beginning of the while loop
            continue

        if 'Failed password' in line:    # If the line contains 'Failed password', call the extract_ip 
            found_ip = extract_ip(line)  # function and store the return in the found_ip variable
            
            if found_ip != None:         # This if avoids allocating a None return from the extract_ip function
                
                if found_ip not in ip_counts:
                    ip_counts[found_ip] = 1    # If the found_ip is not already in the dictionary, add it with 1 value
                else:
                    ip_counts[found_ip] += 1   # If the found_ip is already in the dictionary, increment it by 1

                if ip_counts[found_ip] >= MAX_ATTEMPTS:   # When an IP address is detected 5 times or more, send alert
                    send_alert(found_ip, ip_counts[found_ip], URL=WEBHOOK_URL)
            else:
                continue

if __name__ == '__main__':
    main()
