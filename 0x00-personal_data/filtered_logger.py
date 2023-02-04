#!/usr/bin/env python3
"""Module: filtered_logger.py"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    msg = message
    for field in fields:
        msg = re.sub(r'({}=)[a-zA-Z0-9/]+{}'.format(field, separator), r'\1{};'.format(redaction), msg)
    return msg
