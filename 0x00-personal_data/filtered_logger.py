#!/usr/bin/env python3
"""
Definition of filter_datum function that returns an obfuscated log message
"""
import logging
import re
from typing import List


def filter_datum(fields: str, redaction: str, message: str, separator: str) ->\
                                                                        str:
    """
    Function that that returns the log message obfuscated
    Args:
    fields: (list): list of strings indicating fields to obfuscate
    redaction (str): what the field will be obfuscated to
    message (str): the log line to obfuscate
    separator (str): the character separating the fields
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: str):
        """
        Class initialization
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        redact the message of LogRecord instance
        Args:
        record (logging.LogRecord): LogRecord instance containing message
        Return: formatted string
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Function that creates and configures the logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = streamHandler()
    stream_handler.setFormatter(formatter)
    logger.addhandler(stream_handler)

    return logger


PII_FIELDS = ("name", "email", "phone", "password", "ip")
