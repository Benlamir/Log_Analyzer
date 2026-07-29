# Log Analyzer and Automated Alerts

## 1. Business Problem Solved
[cite_start]This tool demonstrates practical system diagnosis and a fundamental understanding of security, specifically access management[cite: 28]. 

## 2. Technical Functionality
* [cite_start]The application runs in the background and monitors a critical Linux server log file, such as `/var/log/auth.log` or Nginx container logs, in real-time[cite: 24, 39].
* [cite_start]It uses regular expressions (the `re` module) to extract the IP address and timestamp specifically from failed connection attempts[cite: 40].
* [cite_start]The script stores problematic IP addresses in a data structure, such as a dictionary, to count their occurrences[cite: 41].
* [cite_start]It detects anomalies by isolating malicious IP addresses once an alert threshold (e.g., 5 failed attempts from the same IP) is reached[cite: 24, 25, 42].
* [cite_start]An automated notification containing a JSON payload (with the targeted IP, date, and time) is sent via an HTTP POST request to a Discord Webhook channel[cite: 26, 46].

## 3. Prerequisites and Setup
* [cite_start]**Environment**: A Linux Virtual Machine (e.g., Ubuntu via VirtualBox) or Windows Subsystem for Linux (WSL) is required[cite: 32].
* [cite_start]**Permissions**: Understanding of Linux permissions (`chmod`, `chown`) is necessary to allow the script to securely read system logs located in `/var/log/`[cite: 35, 36].
* [cite_start]**Security Note**: The Discord Webhook URL must never be hardcoded into the script[cite: 51]. [cite_start]It must be retrieved via an environment variable using the `os` module[cite: 52].

## 4. Execution and Usage
* [cite_start]**Testing**: Before running on a live system, generate a fake `auth.log` file in the user space and manually insert typical log lines (successful connections and failedbattempts) to safely test the script[cite: 33, 34].
* [cite_start]**Production**: To make the script autonomous, execute it in the background using native Linux tools[cite: 47]. [cite_start]This can be achieved by setting up a cron job or creating a basic systemd service[cite: 48].

## 5. Architecture

![Diagramme de séquence de l'analyseur de logs](docs/diagrams/Sequence_Diagram_LogAnalyzer.webp)
 
