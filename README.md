📌 Project Overview

SQL Injection (SQLi) is a web application vulnerability that occurs when untrusted user input is improperly handled and becomes part of a database query.

This project demonstrates a controlled approach to identifying potential SQL injection indicators by:

Accepting a target URL containing query parameters
Establishing an authenticated session with DVWA
Testing URL parameters with controlled SQL injection payloads
Analyzing HTTP responses for database error indicators
Performing multiple tests using basic concurrency
Applying configurable request delays
Recording scan activities through logging
Generating a structured scan report

Important: This scanner is intended only for systems that you own or have explicit permission to test.

🎯 Project Objectives

The main objectives of this project are to:

Understand the fundamentals of SQL Injection.
Demonstrate automated security testing using Python.
Learn how HTTP requests and URL parameters can be analyzed.
Implement authenticated web-session handling.
Detect common database error indicators.
Implement basic concurrency for security testing.
Implement request-rate control using delays.
Generate security testing reports.
Maintain logs of scanner activities.
Demonstrate responsible and ethical cybersecurity practices.
🛠️ Technologies Used
Technology	Purpose
Python	Scanner development
Requests	HTTP communication
argparse	Command-line interface
ThreadPoolExecutor	Basic concurrent scanning
Logging	Scan activity logging
urllib.parse	URL and query parameter processing
Docker	Running the vulnerable testing environment
DVWA	Authorized SQL injection laboratory
MySQL/MariaDB	Database used by the DVWA environment
Visual Studio Code	Development environment
📂 Project Structure
SQL Injection Scanner/
│
├── venv/
│
├── reports/
│   └── scan_report.txt
│
├── screenshots/
│   ├── 01_project_structure.png
│   ├── 02_python_environment.png
│   ├── 03_dependencies.png
│   ├── 04_scanner_help.png
│   ├── 05_dvwa_setup.png
│   ├── 06_dvwa_sql_injection.png
│   ├── 07_scanner_running.png
│   ├── 08_scan_result.png
│   ├── 09_scan_report.png
│   └── 10_scanner_log.png
│
├── scanner.py
├── payloads.py
├── detector.py
├── reporter.py
├── requirements.txt
├── scanner.log
├── README.md
└── .gitignore
🧩 Project Components
scanner.py

The main application responsible for:

Processing command-line arguments
Establishing a DVWA session
Authenticating users
Discovering URL parameters
Sending SQL injection test payloads
Running concurrent tests
Applying request delays
Collecting scan results
Generating reports
Recording scan activities
payloads.py

Contains controlled SQL injection test payloads used during the authorized scan.

Example payloads include:

'
"
' OR '1'='1
" OR "1"="1
' AND '1'='2
" AND "1"="2
detector.py

Analyzes HTTP responses and searches for common database-related indicators such as:

mysql
mysqli
postgresql
sqlite
odbc
sql error
database error
reporter.py

Generates the final text-based security scan report containing information about detected potential SQL injection indicators.

requirements.txt

Contains the Python dependency required by the project:

requests==2.34.2
⚙️ Features
1. SQL Injection Payload Testing

The scanner tests URL parameters using controlled SQL injection payloads.

Example:

' OR '1'='1

and:

" AND "1"="2

These payloads are intended for controlled security testing environments.

2. URL Parameter Analysis

The scanner identifies query parameters from URLs such as:

http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit

The scanner identifies:

id
Submit

and excludes the Submit parameter from SQL injection testing.

3. Authenticated Session Support

The scanner can authenticate against the local DVWA login page before performing security tests.

Example:

Login URL: http://127.0.0.1:8080/login.php
Username: admin
Password: password

The authenticated session is maintained using Python's requests.Session().

4. Response Analysis

After sending each test request, the scanner analyzes the response body for database-related indicators.

For example:

mysql

may indicate that the application returned a database-related error.

The scanner reports these as potential SQL injection indicators, rather than automatically declaring the application vulnerable.

5. Basic Concurrency

The project uses Python's:

ThreadPoolExecutor

to perform multiple controlled tests concurrently.

The number of workers can be configured using:

--workers

Example:

--workers 2
6. Request Rate Control

The scanner supports a configurable delay between requests.

Example:

--delay 0.5

This introduces a 0.5-second delay between individual test operations.

7. Logging

Scanner activities are recorded in:

scanner.log

The log can contain:

Scan start
Parameters tested
Payloads tested
Request errors
Scan completion
Number of findings
8. Report Generation

The scanner automatically generates:

reports/scan_report.txt

The report contains:

Scan timestamp
Target URL
Tested parameter
Payload
Detected indicators
🚀 Installation
Prerequisites

Before running the project, install:

Python 3
Docker Desktop
Visual Studio Code
Git

Verify Python:

python --version

Verify Docker:

docker --version
1. Open the Project

Open the project folder in Visual Studio Code.

SQL Injection Scanner
2. Create a Virtual Environment

Run:

python -m venv venv
3. Activate the Virtual Environment

On Windows PowerShell:

.\venv\Scripts\Activate.ps1

The terminal should display something similar to:

(venv) PS C:\...\SQL Injection Scanner>
4. Install Dependencies

Run:

pip install -r requirements.txt

Verify Requests:

pip show requests
🐳 Setting Up DVWA

This project uses Damn Vulnerable Web Application (DVWA) as an intentionally vulnerable local security-testing environment.

Start DVWA with:

docker run --rm -it -p 8080:80 vulnerables/web-dvwa

Open the application:

http://127.0.0.1:8080

Complete the DVWA database setup if required.

Log in using the local training credentials:

Username: admin
Password: password

Set the DVWA security level to:

Low

for the controlled demonstration.

🔍 Testing the SQL Injection Page

Navigate to:

http://127.0.0.1:8080/vulnerabilities/sqli/

Enter:

1

and submit the request.

A successful request should produce a URL similar to:

http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit

This URL contains the id parameter that the scanner can test.

▶️ Running the Scanner

From the project directory, run:

python scanner.py "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --login-url "http://127.0.0.1:8080/login.php" --username "admin" --password "password"

The scanner will:

Connect to the local DVWA application.
Open the DVWA login page.
Authenticate using the supplied credentials.
Establish an authenticated session.
Identify the id parameter.
Send controlled SQL injection payloads.
Analyze HTTP responses.
Display potential findings.
Generate a scan report.
Record activities in the scanner log.
⚙️ Command-Line Options

Display the available options with:

python scanner.py --help

Available options include:

--login-url
--username
--password
--delay
--workers
--output
Example
python scanner.py "http://127.0.0.1:8080/vulnerabilities/sqli/?id=1&Submit=Submit" `
--login-url "http://127.0.0.1:8080/login.php" `
--username "admin" `
--password "password" `
--delay 0.5 `
--workers 2
📊 Example Scan Result

A successful local test produced output similar to:

[!] Potential SQL injection indicator detected
Parameter: id
Payload: " AND "1"="2
Indicators: mysql

============================================================
SCAN COMPLETE
============================================================
Potential findings: 6
Report: reports/scan_report.txt
Log: scanner.log

The detected:

mysql

indicator demonstrates that the scanner identified database-related content in the DVWA response.

The result should be interpreted as a potential indicator, not proof by itself that an arbitrary application is vulnerable.

📄 Generated Report

After the scan, the following file is generated:

reports/scan_report.txt

Example report structure:

SQL INJECTION SCANNER REPORT
============================================================
Scan time: 2026-09-17 12:00:00
============================================================

Finding 1
------------------------------------------------------------
URL: http://127.0.0.1:8080/vulnerabilities/sqli/?id=1%27&Submit=Submit
Parameter: id
Payload: '
Indicators: mysql
📝 Logging

The scanner records activities in:

scanner.log

The log provides a basic audit trail of the testing process.

Example:

INFO - Starting scan against http://127.0.0.1:8080/...
INFO - Testing parameter=id payload='
INFO - Testing parameter=id payload=" OR "1"="1
INFO - Scan completed. Findings=6
📸 Project Screenshots

The screenshots directory documents the development and testing process.

Screenshot	Description
01_project_structure.png	Project directory structure
02_python_environment.png	Python and virtual environment
03_dependencies.png	Installed dependencies
04_scanner_help.png	Scanner command-line help
05_dvwa_setup.png	DVWA local environment
06_dvwa_sql_injection.png	DVWA SQL injection page
07_dvwa_security_setup.png	DVWA SQL injection page
08_scanner_running.png	Scanner execution
09_scan_result.png	Detected scan results
10_scan_report.png	Generated security report
11_scanner_log.png	Scanner activity log

🔐 Security and Ethical Use

This project is strictly intended for:

Cybersecurity education
Authorized penetration testing
Local security laboratories
Academic projects
Internship demonstrations
Intentionally vulnerable applications
Security research conducted with permission

The scanner must not be used against websites, applications, servers, APIs, or databases without explicit authorization.

For this project, testing was performed against a local DVWA environment:

127.0.0.1:8080
🎓 Learning Outcomes

This project demonstrates practical knowledge of:

SQL Injection fundamentals
Web application security
HTTP requests
URL query parameters
Python automation
Authentication sessions
Response analysis
Concurrent programming
Request-rate control
Logging
Report generation
Docker
Vulnerability-testing laboratories
Ethical security testing
🔮 Future Improvements

Potential future improvements include:

POST parameter scanning
Cookie-based authentication support
Additional SQL injection detection techniques
Baseline response comparison
Improved false-positive detection
HTML report generation
JSON report generation
Configurable external payload files
Additional authentication mechanisms
Broader vulnerability detection capabilities
⚠️ Disclaimer

This project is provided for educational and authorized security-testing purposes only.

The developer assumes no responsibility for unauthorized or illegal use of this software.

Always obtain appropriate authorization before conducting security testing against a system.

👨‍💻 Author

Fortune Idorenyin Effiong

Cybersecurity & Cloud Computing Enthusiast

Nigeria

📜 License

This project is intended primarily for educational and authorized security-testing purposes.
If redistributed or modified, users should retain the project's ethical-use and authorization requirements.