"""
Response analysis functions.
"""

ERROR_INDICATORS = [
    "sql syntax",
    "mysql",
    "mysqli",
    "postgresql",
    "postgres",
    "sqlite",
    "sqlite3",
    "odbc",
    "database error",
    "sql error",
    "ora-",
    "microsoft sql server",
]


def detect_sql_error(response_text):
    """Find common database error indicators."""

    response_lower = response_text.lower()

    findings = []

    for indicator in ERROR_INDICATORS:
        if indicator in response_lower:
            findings.append(indicator)

    return findings