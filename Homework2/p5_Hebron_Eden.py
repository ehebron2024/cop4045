"""
Weather station daily temperature observation analysis.

Each line of the input file has the format:
    station,date,temperature

station is a string, date is a timestamp string such as
"09:28:09 AM 04/20/2026", and temperature is a float that is only
valid when it lies between -100.0 and 150.0 inclusive.
"""

import csv
import sys
from datetime import datetime
from typing import Dict, List, Tuple

Observations = Dict[str, List[Tuple[datetime, float]]]
StationStatistics = Dict[str, Dict[str, float]]

DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
MIN_TEMP = -100.0
MAX_TEMP = 150.0


def read_observations(filename: str) -> Tuple[Observations, List[Tuple[int, str]]]:
    """
    Read daily temperature observations for one or more weather stations.

    Args:
        filename: Path of the input file. Each line has the format
            "station,date,temperature".

    Returns:
        A tuple (observations, errors):
            observations: dict mapping each station name to a list of
                (date, temperature) tuples, sorted by date. date is a
                datetime.datetime object and temperature is a float.
            errors: list of (line_number, error_message) tuples for
                every line that was rejected (malformed lines, invalid
                temperatures, and duplicate station/date combinations).
                Empty if there were no errors. Line numbers start at 1.

    Raises:
        FileNotFoundError: If filename does not exist.
        OSError: For other I/O related errors.
    """
    observations: Observations = {}
    errors: List[Tuple[int, str]] = []
    seen = set()  # (station, date) pairs already recorded

    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            for line_number, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line:
                    continue

                fields = line.split(",")
                if len(fields) != 3:
                    errors.append((line_number,
                                    f"Malformed line (expected 3 fields, got {len(fields)}): '{line}'"))
                    continue

                station, date_str, temp_str = (field.strip() for field in fields)

                if not station:
                    errors.append((line_number, "Malformed line: missing station name"))
                    continue

                try:
                    date = datetime.strptime(date_str, DATE_FORMAT)
                except ValueError:
                    errors.append((line_number, f"Malformed date: '{date_str}'"))
                    continue

                try:
                    temperature = float(temp_str)
                except ValueError:
                    errors.append((line_number, f"Malformed temperature: '{temp_str}'"))
                    continue

                if not (MIN_TEMP <= temperature <= MAX_TEMP):
                    errors.append((line_number,
                                    f"Invalid temperature {temperature} "
                                    f"(must be between {MIN_TEMP} and {MAX_TEMP})"))
                    continue

                key = (station, date)
                if key in seen:
                    errors.append((line_number,
                                    f"Duplicate observation for station '{station}' at {date}"))
                    continue
                seen.add(key)

                observations.setdefault(station, []).append((date, temperature))

        for station_observations in observations.values():
            station_observations.sort(key=lambda obs: obs[0])

        return observations, errors

    except FileNotFoundError as e:
        print(f"Error: could not read observations — file not found: '{filename}': {e}")
        raise
    except OSError as e:
        print(f"Error: could not read observations from '{filename}': {e}")
        raise


def station_statistics(observations: Observations) -> StationStatistics:
    if not isinstance(observations, dict):
        raise TypeError("observations must be a dictionary")

    statistics: StationStatistics = {}

    for station, obs_list in observations.items():
        if not obs_list:
            continue

        temperatures = [temperature for _, temperature in obs_list]
        statistics[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures),
        }

    return statistics


def station_outliers(observations: Observations) -> Dict[str, Tuple[datetime, float, float]]:
    """
    Find stations whose latest reported temperature is an outlier.

    A station is an outlier if its latest reported temperature (the
    observation with the most recent date) exceeds its mean
    temperature, as computed by station_statistics().

"""
    if not isinstance(observations, dict):
        raise TypeError("observations must be a dictionary")

    statistics = station_statistics(observations)

    return {
        station: (obs_list[-1][0], obs_list[-1][1], statistics[station]["mean"])
        for station, obs_list in observations.items()
        if obs_list and obs_list[-1][1] > statistics[station]["mean"]
    }


def write_statistics(filename: str, statistics: StationStatistics) -> None:
    """
    Write station statistics to a CSV file in lexicographic order.

    Stations are written in lexicographic (alphabetical) order of
    their names. For each station, its statistic fields ('max',
    'mean', 'min') are also written in lexicographic order of their
    field names. Every numeric value is formatted with exactly one
    digit after the decimal point.

    Args:
        filename: Path of the output CSV file.
        statistics: dict mapping station name to a dict with keys
            'min', 'max', and 'mean', such as returned by
            station_statistics().

    Raises:
        TypeError: If statistics is not a dictionary.
        OSError: For I/O related errors.
    """
    if not isinstance(statistics, dict):
        raise TypeError("statistics must be a dictionary")

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["station", "max", "mean", "min"])
            for station in sorted(statistics):
                stats = statistics[station]
                row = [station] + [f"{stats[field]:.1f}" for field in sorted(stats)]
                writer.writerow(row)

    except OSError as e:
        print(f"Error: could not write statistics to '{filename}': {e}")
        raise


def main() -> None:
    """
    Command-line entry point.

    Usage:
        python3 p5_Hebron_Eden.py <input_file> <output_file>

    Reads daily temperature observations from <input_file>, prints
    station statistics and outliers to the terminal, and writes the
    statistics to <output_file>. File access errors (missing file,
    permission errors, bad directory, etc.) are caught and reported;
    the program then exits with a non-zero status instead of crashing
    with a traceback.
    """
    print("fau id: Ehebron2024")

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except OSError:
        sys.exit(1)

    print("\nErrors:")
    if not errors:
        print("  (none)")
    for line_number, message in errors:
        print(f"  line {line_number}: {message}")

    statistics = station_statistics(observations)
    print("\nStation statistics:")
    for station in sorted(statistics):
        stats = statistics[station]
        print(f"  {station}: min={stats['min']:.1f}, max={stats['max']:.1f}, "
              f"mean={stats['mean']:.1f}")

    outliers = station_outliers(observations)
    print("\nStation outliers:")
    if not outliers:
        print("  (none)")
    for station in sorted(outliers):
        date, temperature, mean = outliers[station]
        print(f"  {station}: latest={temperature:.1f} on {date}, mean={mean:.1f}")

    try:
        write_statistics(output_filename, statistics)
    except OSError:
        sys.exit(1)

    print(f"\nStatistics written to '{output_filename}'.")


if __name__ == "__main__":
    main()
