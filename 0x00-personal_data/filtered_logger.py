#!/usr/bin/env python3
"""Module: filtered_logger.py"""
from typing import List
import logging
import mysql
import bcrypt
import re
from os import getenv

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
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db():
    """retruns connector to database"""
    user = getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    password = getenv('PERSONAL_DATA_DB_USERNAME') or ""
    host = getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = getenv('PERSONAL_DATA_DB_NAME')

    connect = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=db_name
            )
    return connect


def main():
    """executes sql commands"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".fomat(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


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
