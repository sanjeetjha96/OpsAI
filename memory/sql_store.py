"""Placeholder for a more advanced SQL-backed memory store (e.g., Postgres).

This file contains a small class that mirrors MemoryStore API and can be
extended with connection pooling and migrations for production use.
"""
from typing import Any, Dict, Optional


class SQLMemoryStore:
    def __init__(self, dsn: str):
        # For now this is a placeholder. In production, use asyncpg/psycopg2.
        self.dsn = dsn

    def add(self, mem_type: str, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> int:
        raise NotImplementedError("SQLMemoryStore is a scaffold; implement for your DB")
