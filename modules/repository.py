"""
repository for mod_ahbot table
@author Abracadaniel22
"""
import mysql.connector
from enum import Enum, auto

from .config import config

CURSOR_RESULT_ROW_INSERTED = 1
CURSOR_RESULT_ROW_UPDATED = 2
CURSOR_RESULT_KEPT_SAME = 0

class UpsertResult(Enum):
    INSERTED = auto()
    UPDATED = auto()
    KEPT_SAME = auto()

class Repository:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**{
                'host': config.mysql_host,
                'port': config.mysql_port,
                'database': config.mysql_database,
                'user': config.mysql_user,
                'password': config.mysql_password
            })
        except mysql.connector.Error as e:
            raise RuntimeError("Can't connect to mysql") from e
        
    def count(self):
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError("Cannot perform upsert, no connection.")
        
        with self.connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT COUNT(item_id) FROM mod_ahbot;")
        return cursor.fetchone()[0]

    def upsert(self, item_id: int, min_bid_price: int) -> UpsertResult:
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError("Cannot perform upsert, no connection.")

        sql = """
            INSERT INTO mod_ahbot (item_id, min_bid_price)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                item_id = VALUES(item_id),
                min_bid_price = VALUES(min_bid_price);
        """
        data = (item_id, min_bid_price)

        with self.connection.cursor() as cursor:
            cursor.execute(sql, data)
            self.connection.commit()

            row_count = cursor.rowcount
            if row_count == CURSOR_RESULT_ROW_INSERTED:
                return UpsertResult.INSERTED
            elif row_count == CURSOR_RESULT_ROW_UPDATED:
                return UpsertResult.UPDATED
            elif row_count == CURSOR_RESULT_KEPT_SAME:
                return UpsertResult.KEPT_SAME
            else:
                raise RuntimeError(f"Unexpected rowcount value: {row_count}. item_id: {item_id}, min_bid_price: {min_bid_price}")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()