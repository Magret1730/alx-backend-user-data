#!/usr/bin/env python3
"""Task 0"""
import re


def filter_datum(fields, redaction, message, separator):
    """function that that returns the log message obfuscated"""
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
