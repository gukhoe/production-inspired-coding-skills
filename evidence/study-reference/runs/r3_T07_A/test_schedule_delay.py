import unittest

from schedule_delay import calculate_delay


class ScheduleDelayTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(calculate_delay("2026-11-10", "2026-11-14"), 4)

    def test_on_time(self):
        self.assertEqual(calculate_delay("2026-11-10", "2026-11-10"), 0)

    def test_early_completion(self):
        self.assertEqual(calculate_delay("2026-11-10", "2026-11-08"), 0)

    def test_year_boundary(self):
        self.assertEqual(calculate_delay("2026-12-31", "2027-01-02"), 2)

    def test_leap_year(self):
        self.assertEqual(calculate_delay("2028-02-28", "2028-03-01"), 2)

    def test_invalid_calendar_date(self):
        with self.assertRaises(ValueError):
            calculate_delay("2026-02-29", "2026-03-01")


if __name__ == "__main__":
    unittest.main()
