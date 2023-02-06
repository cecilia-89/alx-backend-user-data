#!/usr/bin/env python3
"""Module: filtered_logger.py"""
from typing import List
import logging
import re

PII_FIELDS = ('name', 'email', 'ssn', 'password', 'ip')

def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(r'({}=).+?{}'.format(field, separator),
                         r'\1{}{}'.format(redaction, separator), message)
    return message


def get_logger():
    """returns a logging.Logger object"""


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns formatted log"""
        formatted = super().format(record)
        message = filter_datum(self.fields, self.REDACTION,
                               formatted, self.SEPARATOR)
        return message
