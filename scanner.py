"""
SQL Injection Scanner

For authorized security testing only.
Designed for local applications and intentionally
vulnerable training environments such as DVWA.
"""

import argparse
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import requests

from payloads import SQL_PAYLOADS
from detector import detect_sql_error
from reporter import generate_report


logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_test_url(url, parameter, value):
    """Create a URL containing a modified parameter value."""

    parsed = urlparse(url)
    query_parameters = parse_qs(parsed.query)

    query_parameters[parameter] = [value]

    new_query = urlencode(query_parameters, doseq=True)

    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )


def login_to_dvwa(session, login_url, username, password):
    """Log into DVWA and establish an authenticated session."""

    print("\nLogging into DVWA...")

    try:
        # Step 1: Open the login page.
        login_page = session.get(
            login_url,
            timeout=10,
        )

        if login_page.status_code != 200:
            print(
                f"[!] Could not open DVWA login page. "
                f"HTTP {login_page.status_code}"
            )
            return False

        # Step 2: Look for DVWA's hidden user_token.
        token_match = re.search(
            r'name=["\']user_token["\']\s+value=["\']([^"\']+)["\']',
            login_page.text,
        )

        user_token = ""

        if token_match:
            user_token = token_match.group(1)

        # Step 3: Submit the login form.
        login_data = {
            "username": username,
            "password": password,
            "Login": "Login",
            "user_token": user_token,
        }

        response = session.post(
            login_url,
            data=login_data,
            timeout=10,
            allow_redirects=True,
        )

        if response.status_code != 200:
            print(
                f"[!] DVWA login returned "
                f"HTTP {response.status_code}"
            )
            return False

        # Step 4: Verify the authenticated session.
        home_url = "http://127.0.0.1:8080/index.php"

        home_response = session.get(
            home_url,
            timeout=10,
        )

        if "You have logged in as" in home_response.text:
            print("[+] DVWA login successful.")
            return True

        if "Logout" in home_response.text:
            print("[+] DVWA login successful.")
            return True

        print("[!] DVWA login could not be verified.")

        return False

    except requests.RequestException as error:
        print(f"[!] DVWA login failed: {error}")

        logging.error(
            "DVWA login failed: %s",
            error,
        )

        return False


def scan_parameter(
    session,
    url,
    parameter,
    original_value,
    payload,
    delay,
):
    """Test one parameter with one SQL injection payload."""

    time.sleep(delay)

    test_url = create_test_url(
        url,
        parameter,
        original_value + payload,
    )

    logging.info(
        "Testing parameter=%s payload=%s",
        parameter,
        payload,
    )

    try:
        response = session.get(
            test_url,
            timeout=10,
        )

        indicators = detect_sql_error(response.text)

        if indicators:
            return {
                "url": test_url,
                "parameter": parameter,
                "payload": payload,
                "indicators": indicators,
            }

    except requests.RequestException as error:
        logging.error(
            "Request failed: %s",
            error,
        )

    return None


def scan_url(
    session,
    url,
    delay,
    workers,
):
    """Scan parameters contained in the URL."""

    parsed = urlparse(url)
    parameters = parse_qs(parsed.query)

    if not parameters:
        print("\nNo URL parameters were found.")
        return []

    results = []
    tasks = []

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        for parameter, values in parameters.items():

            original_value = values[0]

            # Do not scan the Submit button parameter.
            if parameter.lower() == "submit":
                continue

            for payload in SQL_PAYLOADS:

                task = executor.submit(
                    scan_parameter,
                    session,
                    url,
                    parameter,
                    original_value,
                    payload,
                    delay,
                )

                tasks.append(task)

        for task in as_completed(tasks):

            result = task.result()

            if result:

                results.append(result)

                print(
                    "\n[!] Potential SQL injection indicator detected"
                )

                print(
                    f"Parameter: {result['parameter']}"
                )

                print(
                    f"Payload: {result['payload']}"
                )

                print(
                    f"Indicators: "
                    f"{', '.join(result['indicators'])}"
                )

            else:

                print(".", end="", flush=True)

    return results


def main():

    parser = argparse.ArgumentParser(
        description=(
            "SQL Injection Scanner for authorized "
            "local testing."
        )
    )

    parser.add_argument(
        "url",
        help=(
            "Authorized target URL containing "
            "query parameters."
        ),
    )

    parser.add_argument(
        "--login-url",
        default=None,
        help="DVWA login URL.",
    )

    parser.add_argument(
        "--username",
        default=None,
        help="DVWA username.",
    )

    parser.add_argument(
        "--password",
        default=None,
        help="DVWA password.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Number of concurrent workers.",
    )

    parser.add_argument(
        "--output",
        default="reports/scan_report.txt",
        help="Report output file.",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("SQL INJECTION SCANNER")
    print("=" * 60)

    print("\nAuthorized testing only.")
    print(f"Target: {args.url}")
    print(f"Delay: {args.delay} seconds")
    print(f"Workers: {args.workers}")

    session = requests.Session()

    if (
        args.login_url
        and args.username
        and args.password
    ):

        login_success = login_to_dvwa(
            session,
            args.login_url,
            args.username,
            args.password,
        )

        if not login_success:

            print(
                "\nScan stopped because DVWA login failed."
            )

            return

    logging.info(
        "Starting scan against %s",
        args.url,
    )

    results = scan_url(
        session,
        args.url,
        args.delay,
        args.workers,
    )

    generate_report(
        results,
        args.output,
    )

    logging.info(
        "Scan completed. Findings=%d",
        len(results),
    )

    print("\n")
    print("=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)

    print(
        f"Potential findings: {len(results)}"
    )

    print(
        f"Report: {args.output}"
    )

    print("Log: scanner.log")


if __name__ == "__main__":
    main()