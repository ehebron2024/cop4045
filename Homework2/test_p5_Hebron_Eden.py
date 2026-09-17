"""
Unit tests for p5_Hebron_Eden.py (weather station temperature analysis).
"""

import os
import shutil
import tempfile
import unittest
from datetime import datetime

from p5_Hebron_Eden import (
    read_observations,
    station_statistics,
    write_statistics,
)


class TestWeatherStationAnalysis(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _write_input_file(self, lines):
        path = os.path.join(self.temp_dir, "input.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return path

    def test_multiple_stations_are_grouped_separately(self):
        path = self._write_input_file([
            "Station A,09:00:00 AM 01/01/2026,50.0",
            "Station B,10:00:00 AM 01/01/2026,60.0",
            "Station C,11:00:00 AM 01/01/2026,70.0",
        ])
        observations, errors = read_observations(path)

        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {"Station A", "Station B", "Station C"})
        self.assertEqual(observations["Station A"][0][1], 50.0)
        self.assertEqual(observations["Station B"][0][1], 60.0)
        self.assertEqual(observations["Station C"][0][1], 70.0)

    def test_negative_temperatures_within_range_are_accepted(self):
        path = self._write_input_file([
            "Station A,09:00:00 AM 01/01/2026,-99.9",
            "Station A,10:00:00 AM 01/01/2026,-50.0",
        ])
        observations, errors = read_observations(path)

        self.assertEqual(errors, [])
        temperatures = [temp for _, temp in observations["Station A"]]
        self.assertEqual(temperatures, [-99.9, -50.0])

    def test_duplicate_station_date_combination_is_rejected(self):
        path = self._write_input_file([
            "Station A,09:00:00 AM 01/01/2026,50.0",
            "Station A,09:00:00 AM 01/01/2026,55.0",  # duplicate station/date
        ])
        observations, errors = read_observations(path)

        self.assertEqual(len(observations["Station A"]), 1)
        self.assertEqual(observations["Station A"][0][1], 50.0)
        self.assertEqual(len(errors), 1)
        line_number, message = errors[0]
        self.assertEqual(line_number, 2)
        self.assertIn("Duplicate", message)

    def test_temperature_outside_valid_range_is_rejected(self):
        path = self._write_input_file([
            "Station A,09:00:00 AM 01/01/2026,-100.0",   # valid boundary
            "Station A,10:00:00 AM 01/01/2026,150.0",    # valid boundary
            "Station A,11:00:00 AM 01/01/2026,-100.1",   # invalid: too low
            "Station A,12:00:00 PM 01/01/2026,150.1",    # invalid: too high
        ])
        observations, errors = read_observations(path)

        temperatures = [temp for _, temp in observations["Station A"]]
        self.assertEqual(temperatures, [-100.0, 150.0])
        self.assertEqual(len(errors), 2)
        self.assertEqual([line_number for line_number, _ in errors], [3, 4])

    def test_station_statistics_computes_min_max_mean(self):
        observations = {
            "Station A": [
                (datetime(2026, 1, 1, 9, 0, 0), 10.0),
                (datetime(2026, 1, 1, 10, 0, 0), 20.0),
                (datetime(2026, 1, 1, 11, 0, 0), 30.0),
            ]
        }
        statistics = station_statistics(observations)

        self.assertEqual(statistics["Station A"]["min"], 10.0)
        self.assertEqual(statistics["Station A"]["max"], 30.0)
        self.assertEqual(statistics["Station A"]["mean"], 20.0)

    def test_write_statistics_orders_stations_and_fields_lexicographically(self):
        statistics = {
            "Station B": {"min": 1.0, "max": 2.0, "mean": 1.5},
            "Station A": {"min": 2.34, "max": 4.999, "mean": 3.777},
        }
        path = os.path.join(self.temp_dir, "stats.csv")
        write_statistics(path, statistics)

        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        self.assertEqual(lines[0], "station,max,mean,min")
        self.assertEqual(lines[1], "Station A,5.0,3.8,2.3")
        self.assertEqual(lines[2], "Station B,2.0,1.5,1.0")

    def test_read_observations_missing_file_raises_file_not_found_error(self):
        missing_path = os.path.join(self.temp_dir, "does_not_exist.csv")
        with self.assertRaises(FileNotFoundError):
            read_observations(missing_path)


if __name__ == "__main__":
    unittest.main()
