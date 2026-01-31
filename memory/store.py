"""Simple persistent memory store using sqlite3 for prototyping."""
import json
import os
import sqlite3
import time
from typing import Any, Dict, List, Optional

DB_PATH = os.path.join("memory", "memory.db")


class MemoryStore:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mem_type TEXT,
                content TEXT,
                metadata TEXT,
                created_at REAL
            )
            """
        )
        self.conn.commit()

    def add(self, mem_type: str, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO memories (mem_type, content, metadata, created_at) VALUES (?, ?, ?, ?)",
            (mem_type, json.dumps(content), json.dumps(metadata or {}), time.time()),
        )
        self.conn.commit()
        return cur.lastrowid

    def query(self, mem_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        if mem_type:
            cur.execute("SELECT id, mem_type, content, metadata, created_at FROM memories WHERE mem_type=? ORDER BY created_at DESC LIMIT ?", (mem_type, limit))
        else:
            cur.execute("SELECT id, mem_type, content, metadata, created_at FROM memories ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [
            {"id": r[0], "mem_type": r[1], "content": json.loads(r[2]), "metadata": json.loads(r[3]), "created_at": r[4]}
            for r in rows
        ]

    def delete(self, mem_id: int) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM memories WHERE id=?", (mem_id,))
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


if __name__ == "__main__":
    store = MemoryStore()
    print("Adding sample episodic memory...")
    mid = store.add("episodic", {"title": "sample", "text": "an incident happened"}, {"severity": "low"})
    print("Added id:", mid)
    print("Querying memories:", store.query())
