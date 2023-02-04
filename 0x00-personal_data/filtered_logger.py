#!/usr/bin/env python3
"""Module: filtered_logger.py"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(r'({}=).+?{}'.format(field, separator),
                     r'\1{};'.format(redaction), message)
    return message
