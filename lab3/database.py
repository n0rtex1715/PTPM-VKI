"""Класс работы с базой данных (SQLite)."""
import sqlite3


class Database:
    def __init__(self, path=":memory:"):
        self._conn = sqlite3.connect(path)
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS triangles (
                side1 TEXT NOT NULL,
                side2 TEXT NOT NULL,
                side3 TEXT NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (side1, side2, side3)
            )"""
        )
        self._conn.commit()

    def add_record(self, a, b, c, triangle_type, error_message=""):
        self._conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (str(a), str(b), str(c), triangle_type, error_message or ""),
        )
        self._conn.commit()

    def get_record(self, a, b, c):
        """Возвращает словарь с записью или None, если записи нет."""
        row = self._conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (str(a), str(b), str(c)),
        ).fetchone()
        if row is None:
            return None
        return {"triangle_type": row[0], "error_message": row[1]}

    def delete_record(self, a, b, c):
        """Удаляет запись. Возвращает True, если запись существовала."""
        cur = self._conn.execute(
            "DELETE FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (str(a), str(b), str(c)),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def close(self):
        self._conn.close()
