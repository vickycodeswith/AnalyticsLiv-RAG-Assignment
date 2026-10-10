import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "novatech.db"
DOCS = ROOT / "data" / "documents"


def test_each_table_has_between_50_and_200_rows():
    with sqlite3.connect(DB) as conn:
        for table in ("projects", "employees", "support_tickets"):
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            assert 50 <= count <= 200


def test_foreign_keys_are_valid():
    with sqlite3.connect(DB) as conn:
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert conn.execute("SELECT COUNT(*) FROM employees e LEFT JOIN projects p ON e.project_id=p.project_id WHERE p.project_id IS NULL").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM support_tickets t LEFT JOIN employees e ON t.employee_id=e.employee_id WHERE e.employee_id IS NULL").fetchone()[0] == 0


def test_documents_include_multiple_file_types():
    suffixes = {p.suffix.lower() for p in DOCS.iterdir() if p.is_file()}
    assert len([p for p in DOCS.iterdir() if p.is_file()]) >= 5
    assert {".pdf", ".docx", ".txt"}.issubset(suffixes)
