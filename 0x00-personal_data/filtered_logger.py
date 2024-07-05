#!/usr/bin/env python3
"""
Definition of filter_datum function that returns an obfuscated log message
"""
import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "password", "ssn")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
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

    def __init__(self, fields: List[str]):
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
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Database connection using environment variables
    """
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
                    user=username,
                    password=password,
                    host=host,
                    database=database)
    return connection


def main():
    """
    Main function that retrieves all rows in the users table
    and displays each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        for row in cursor:
            row_str = '; '.join(f"{k}={v}" for k, v in row.items())
            logger.info(row_str)
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
