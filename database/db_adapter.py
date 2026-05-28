"""
db_adapter.py — Database abstraction for SQLite (local) and PostgreSQL (Vercel).

Usage in app.py:
    from database.db_adapter import get_db, init_db_if_needed

The returned connection object is context-manager-compatible (supports `with`).
For PostgreSQL, autocommit is left off and the context manager commits on exit.
"""
import os
import sqlite3

# Detect environment
DATABASE_URL = os.environ.get('DATABASE_URL', '')
USE_POSTGRES = bool(DATABASE_URL)

# ── SQLite path (local) ───────────────────────────────────────────────────────
_SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'checklists.db')


# ── PostgreSQL connection wrapper ─────────────────────────────────────────────
class _PgConnection:
    """Thin wrapper around a psycopg2 connection that mimics the sqlite3 interface
    well enough for the existing app code (row_factory, context manager, execute,
    executescript via explicit multi-statement handling)."""

    def __init__(self, raw_conn):
        self._conn = raw_conn
        self._conn.autocommit = False

    # ---- Row factory compatible with dict(row) and row['column'] ----
    class _Row(dict):
        def __getitem__(self, key):
            if isinstance(key, int):
                return list(self.values())[key]
            return super().__getitem__(key)

        def keys(self):
            return super().keys()

    def _make_cursor(self):
        import psycopg2.extras
        cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return cur

    def execute(self, sql, params=()):
        sql = self._translate(sql)
        # For INSERT statements without RETURNING, add RETURNING id so that
        # lastrowid works exactly as with SQLite's cursor.lastrowid.
        is_insert = sql.strip().upper().startswith('INSERT')
        needs_returning = is_insert and 'RETURNING' not in sql.upper()
        if needs_returning:
            sql = sql.rstrip().rstrip(';') + ' RETURNING id'
        cur = self._make_cursor()
        cur.execute(sql, params)
        return _PgCursor(cur)

    def executescript(self, script):
        """Execute a multi-statement SQL script (used for schema init).
        Skips SQLite-specific pragmas."""
        cur = self._conn.cursor()
        for statement in script.split(';'):
            stmt = statement.strip()
            if not stmt:
                continue
            # Skip SQLite-only constructs
            if stmt.upper().startswith('PRAGMA'):
                continue
            try:
                cur.execute(stmt)
            except Exception as e:
                self._conn.rollback()
                raise RuntimeError(f'Schema init error on: {stmt!r}') from e
        self._conn.commit()

    @staticmethod
    def _translate(sql):
        """Convert SQLite idioms to PostgreSQL."""
        # Parameter placeholder
        sql = sql.replace('?', '%s')
        # datetime('now') → NOW()
        sql = sql.replace("datetime('now')", 'NOW()')
        return sql

    # Context manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        return False  # do not suppress exceptions

    def close(self):
        self._conn.close()


class _PgCursor:
    """Wraps a psycopg2 RealDictCursor to expose .lastrowid and .fetchall()."""

    def __init__(self, cur):
        self._cur = cur

    @property
    def lastrowid(self):
        # After INSERT ... RETURNING id, lastrowid is available as first column
        row = self._cur.fetchone()
        if row:
            return list(row.values())[0]
        return None

    def fetchone(self):
        row = self._cur.fetchone()
        if row is None:
            return None
        return dict(row)

    def fetchall(self):
        rows = self._cur.fetchall()
        # Wrap each row so row['col'] and row[0] both work
        result = []
        for r in rows:
            d = dict(r)

            class _R(dict):
                def __getitem__(self_, key):
                    if isinstance(key, int):
                        return list(self_.values())[key]
                    return super().__getitem__(key)

            result.append(_R(d))
        return result

    def __getitem__(self, key):
        return self._cur[key]


# ── Public API ────────────────────────────────────────────────────────────────

def get_db():
    """Return a database connection (SQLite or PostgreSQL)."""
    if USE_POSTGRES:
        import psycopg2
        raw = psycopg2.connect(DATABASE_URL)
        return _PgConnection(raw)
    else:
        conn = sqlite3.connect(_SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn


def init_db_if_needed():
    """Initialise the database schema if it hasn't been set up yet.

    For SQLite: runs schema.sql (same as before).
    For PostgreSQL: runs schema_pg.sql.
    """
    schema_dir = os.path.dirname(__file__)

    if USE_POSTGRES:
        schema_file = os.path.join(schema_dir, 'schema_pg.sql')
    else:
        os.makedirs(schema_dir, exist_ok=True)
        schema_file = os.path.join(schema_dir, 'schema.sql')

    with get_db() as conn:
        with open(schema_file) as f:
            conn.executescript(f.read())
