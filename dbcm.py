import pymysql

class UseDatabase:
    """Context manager for PyMySQL database connections."""

    def __init__(self, db_config):
        self.db_config = db_config

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.db_config["host"],
            port=int(self.db_config.get("port", 3306)),
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()
