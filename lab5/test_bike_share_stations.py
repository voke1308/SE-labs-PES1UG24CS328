"""Regression checks for the corrected station manager."""

import sqlite3
import unittest
from unittest.mock import patch

import bike_share_stations as manager


class StationTests(unittest.TestCase):
    """Exercise station operations and the security-sensitive changes."""

    def setUp(self):
        manager.CONNECTION.execute("DELETE FROM stations")

    def test_parameterized_station_name(self):
        name = "O'Brien'); DROP TABLE stations; --"
        manager.add_station(name, 3, 2)
        row = manager.CONNECTION.execute(
            "SELECT name FROM stations"
        ).fetchone()
        self.assertEqual(row[0], name)

    def test_default_logs_are_independent(self):
        first = manager.add_station("A", 1, 1)
        second = manager.add_station("B", 1, 1)
        self.assertEqual(first, ["A"])
        self.assertEqual(second, ["B"])

    def test_explicit_log_is_preserved(self):
        log = ["existing"]
        self.assertIs(manager.add_station("A", 1, 1, log), log)
        self.assertEqual(log, ["existing", "A"])

    def test_rental_decrements_and_stops_at_zero(self):
        manager.add_station("A", 2, 1)
        station_id = manager.CONNECTION.execute(
            "SELECT id FROM stations"
        ).fetchone()[0]
        self.assertTrue(manager.rent_bike(station_id))
        self.assertFalse(manager.rent_bike(station_id))
        self.assertFalse(manager.has_bikes(station_id))

    def test_missing_station(self):
        self.assertFalse(manager.rent_bike(-1))
        self.assertFalse(manager.has_bikes(-1))
        manager.reset_station(-1)

    def test_null_bike_count(self):
        manager.add_station("A", 1, None)
        station_id = manager.CONNECTION.execute(
            "SELECT id FROM stations"
        ).fetchone()[0]
        self.assertFalse(manager.has_bikes(station_id))

    def test_full_stations_and_reset(self):
        manager.add_station("Full", 2, 2)
        manager.add_station("Partial", 3, 1)
        self.assertEqual(manager.full_stations(), ["Full"])
        station_id = manager.CONNECTION.execute(
            "SELECT id FROM stations WHERE name = ?", ("Full",)
        ).fetchone()[0]
        manager.reset_station(station_id)
        self.assertEqual(manager.full_stations(), [])
        self.assertFalse(manager.has_bikes(station_id))

    def test_pin_boundaries_use_secrets(self):
        with patch.object(manager.secrets, "randbelow", return_value=0) as rng:
            self.assertEqual(manager.unlock_pin(), 1000)
            rng.assert_called_once_with(9000)
        with patch.object(manager.secrets, "randbelow", return_value=8999):
            self.assertEqual(manager.unlock_pin(), 9999)

    def test_database_errors_are_visible(self):
        with patch.object(manager, "CONNECTION") as connection:
            connection.execute.side_effect = sqlite3.OperationalError("test")
            with self.assertRaises(sqlite3.OperationalError):
                manager.reset_station(1)

    def test_import_does_not_run_demo(self):
        # A fresh subprocess must import without creating demonstration rows.
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-c", "import bike_share_stations as m; "
             "print(m.CONNECTION.execute('SELECT COUNT(*) FROM stations')"
             ".fetchone()[0])"],
            check=True, capture_output=True, text=True,
        )
        self.assertEqual(result.stdout.strip(), "0")


if __name__ == "__main__":
    unittest.main()
