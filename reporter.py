"""
Report generation functions.
"""

from datetime import datetime


def generate_report(results, output_file):
    """Generate a text report."""

    with open(output_file, "w", encoding="utf-8") as file:

        file.write("SQL INJECTION SCANNER REPORT\n")
        file.write("=" * 60 + "\n")
        file.write(
            f"Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        file.write("=" * 60 + "\n\n")

        if not results:
            file.write(
                "No potential SQL injection indicators detected.\n"
            )
            return

        for number, result in enumerate(results, start=1):

            file.write(f"Finding {number}\n")
            file.write("-" * 60 + "\n")
            file.write(f"URL: {result['url']}\n")
            file.write(f"Parameter: {result['parameter']}\n")
            file.write(f"Payload: {result['payload']}\n")
            file.write(
                f"Indicators: {', '.join(result['indicators'])}\n"
            )
            file.write("\n")