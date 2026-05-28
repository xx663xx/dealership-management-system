import sqlite3
import unittest

from app.config import REPORTS
from app.contracts import get_sale_contract_data, render_contract
from app.database import init_db


EXPECTED_TABLES = {
    "suppliers",
    "cars",
    "clients",
    "employees",
    "sales",
    "reservations",
    "test_drives",
    "service_orders",
}


def create_test_connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    return conn


class DatabaseSmokeTests(unittest.TestCase):
    def setUp(self):
        self.conn = create_test_connection()

    def tearDown(self):
        self.conn.close()

    def test_schema_creates_all_business_tables(self):
        rows = self.conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

        table_names = {row[0] for row in rows}

        self.assertTrue(EXPECTED_TABLES.issubset(table_names))

    def test_seed_data_populates_core_reference_tables(self):
        expected_counts = {
            "suppliers": 15,
            "cars": 24,
            "clients": 20,
            "employees": 15,
            "sales": 15,
            "reservations": 3,
            "test_drives": 18,
            "service_orders": 15,
        }

        for table_name, expected_count in expected_counts.items():
            with self.subTest(table=table_name):
                actual_count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                self.assertEqual(actual_count, expected_count)

    def test_report_queries_execute_with_default_parameters(self):
        for report_name, report in REPORTS.items():
            with self.subTest(report=report_name):
                params = [param["default"] for param in report.get("params", [])]
                rows = self.conn.execute(report["sql"], params).fetchall()
                self.assertIsInstance(rows, list)

    def test_sale_contract_data_renders_from_template(self):
        data = get_sale_contract_data(self.conn, 1)

        self.assertIsNotNone(data)
        self.assertEqual(data["contract_number"], "ДП-0001")

        contract_text = render_contract(data)

        self.assertIn("ДП-0001", contract_text)
        self.assertIn("Иван Петров", contract_text)
        self.assertIn("Lada", contract_text)

    def test_invalid_car_price_is_rejected_by_schema(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                """
                INSERT INTO cars (supplier_id, brand, model, year, mileage, color, price, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (1, "Test", "Invalid", 2024, 0, "white", -1, "доступна"),
            )


if __name__ == "__main__":
    unittest.main()
