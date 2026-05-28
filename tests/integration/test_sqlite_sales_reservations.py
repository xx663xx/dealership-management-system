import sqlite3
import unittest

from app.database import init_db


def create_test_connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn)
    return conn


class SalesReservationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.conn = create_test_connection()

    def tearDown(self):
        self.conn.close()

    def car_status(self, car_id):
        return self.conn.execute(
            "SELECT status FROM cars WHERE car_id = ?",
            (car_id,),
        ).fetchone()[0]

    def reservation_status(self, reservation_id):
        return self.conn.execute(
            "SELECT status FROM reservations WHERE reservation_id = ?",
            (reservation_id,),
        ).fetchone()[0]

    def test_active_reservation_marks_car_as_reserved(self):
        self.conn.execute(
            """
            INSERT INTO reservations
                (car_id, client_id, employee_id, reservation_date, valid_until, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (19, 6, 3, "2026-05-28", "2026-06-04", "активна"),
        )

        self.assertEqual(self.car_status(19), "забронирована")

    def test_sale_marks_car_as_sold(self):
        self.conn.execute(
            """
            INSERT INTO sales
                (car_id, client_id, employee_id, sale_date, contract_number, sale_price,
                 payment_status, payment_method, payment_date, contract_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (20, 7, 12, "2026-05-28", "ДП-0016", 4050000, "оплачено", "банк", "2026-05-28", None),
        )

        self.assertEqual(self.car_status(20), "продана")

    def test_sale_completes_active_reservation_for_same_car(self):
        self.assertEqual(self.reservation_status(1), "активна")

        self.conn.execute(
            """
            INSERT INTO sales
                (car_id, client_id, employee_id, sale_date, contract_number, sale_price,
                 payment_status, payment_method, payment_date, contract_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (16, 3, 12, "2026-05-28", "ДП-0016", 4200000, "оплачено", "банк", "2026-05-28", None),
        )

        self.assertEqual(self.car_status(16), "продана")
        self.assertEqual(self.reservation_status(1), "завершена")

    def test_database_rejects_second_sale_for_same_car(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                """
                INSERT INTO sales
                    (car_id, client_id, employee_id, sale_date, contract_number, sale_price,
                     payment_status, payment_method, payment_date, contract_file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (1, 2, 2, "2026-05-28", "ДП-DUP", 1400000, "оплачено", "банк", "2026-05-28", None),
            )

    def test_database_rejects_sale_with_unknown_car(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                """
                INSERT INTO sales
                    (car_id, client_id, employee_id, sale_date, contract_number, sale_price,
                     payment_status, payment_method, payment_date, contract_file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (999, 2, 2, "2026-05-28", "ДП-BAD", 1400000, "оплачено", "банк", "2026-05-28", None),
            )


if __name__ == "__main__":
    unittest.main()
