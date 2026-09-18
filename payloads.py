"""
Controlled SQL injection test payloads.

For authorized security testing only.
"""

SQL_PAYLOADS = [
    "'",
    '"',
    "' OR '1'='1",
    '" OR "1"="1',
    "' AND '1'='2",
    '" AND "1"="2',
]