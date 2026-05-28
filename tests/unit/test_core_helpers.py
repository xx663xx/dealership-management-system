import unittest

from packages.dealership_core import format_integer, format_money, safe_contract_filename


class CoreHelperTests(unittest.TestCase):
    def test_format_money_groups_integer_values(self):
        self.assertEqual(format_money(2500000), "2 500 000")

    def test_format_money_keeps_two_decimals_for_fractional_values(self):
        self.assertEqual(format_money("1250.5"), "1 250.50")

    def test_format_money_returns_empty_string_for_none(self):
        self.assertEqual(format_money(None), "")

    def test_format_money_returns_original_text_for_non_numeric_values(self):
        self.assertEqual(format_money("not available"), "not available")

    def test_format_integer_groups_digits(self):
        self.assertEqual(format_integer(42000), "42 000")

    def test_format_integer_returns_empty_string_for_none(self):
        self.assertEqual(format_integer(None), "")

    def test_safe_contract_filename_replaces_unsafe_characters(self):
        self.assertEqual(safe_contract_filename("DP/2026:01 * test"), "DP_2026_01___test")

    def test_safe_contract_filename_uses_fallback_for_empty_result(self):
        self.assertEqual(safe_contract_filename("///"), "contract")


if __name__ == "__main__":
    unittest.main()
