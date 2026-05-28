import unittest

from packages.dealership_core import (
    ValidationError,
    validate_reservation,
    validate_sale,
    validate_test_drive,
)


class CoreValidatorTests(unittest.TestCase):
    def test_validate_sale_accepts_available_car_with_valid_values(self):
        validate_sale("доступна", "2500000", "2026-05-28")

    def test_validate_sale_rejects_unavailable_car(self):
        with self.assertRaisesRegex(ValidationError, "available"):
            validate_sale("продана", "2500000", "2026-05-28")

    def test_validate_sale_rejects_negative_price(self):
        with self.assertRaisesRegex(ValidationError, "non-negative"):
            validate_sale("доступна", "-1", "2026-05-28")

    def test_validate_sale_rejects_invalid_date(self):
        with self.assertRaisesRegex(ValidationError, "YYYY-MM-DD"):
            validate_sale("доступна", "2500000", "28.05.2026")

    def test_validate_sale_rejects_missing_date(self):
        with self.assertRaisesRegex(ValidationError, "sale_date"):
            validate_sale("доступна", "2500000", "")

    def test_validate_reservation_accepts_valid_date_range(self):
        validate_reservation("2026-05-28", "2026-06-02")

    def test_validate_reservation_allows_empty_valid_until(self):
        validate_reservation("2026-05-28", "")

    def test_validate_reservation_rejects_end_date_before_start_date(self):
        with self.assertRaisesRegex(ValidationError, "valid_until"):
            validate_reservation("2026-05-28", "2026-05-27")

    def test_validate_test_drive_accepts_valid_values(self):
        validate_test_drive("2026-05-28", "клиент заинтересован")

    def test_validate_test_drive_rejects_missing_date(self):
        with self.assertRaisesRegex(ValidationError, "test_drive_date"):
            validate_test_drive("", "клиент заинтересован")

    def test_validate_test_drive_rejects_empty_result(self):
        with self.assertRaisesRegex(ValidationError, "result"):
            validate_test_drive("2026-05-28", " ")


if __name__ == "__main__":
    unittest.main()
