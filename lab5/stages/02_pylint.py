"""Manage bike-share stations stored in an in-memory SQLite database."""

import secrets
import sqlite3

CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    "CREATE TABLE stations (id INTEGER PRIMARY KEY, name TEXT, "
    "capacity INTEGER, bikes INTEGER)"
)


def add_station(name, capacity, bikes, log=None):
    """Register a station and return its supplied or newly created name log."""
    if log is None:
        log = []
    CONNECTION.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes),
    )
    log.append(name)
    return log


def rent_bike(station_id):
    """Rent one bike, returning False for missing or empty stations."""
    cursor = CONNECTION.execute(
        "UPDATE stations SET bikes = bikes - 1 WHERE id = ? AND bikes > 0",
        (station_id,),
    )
    return cursor.rowcount == 1


def unlock_pin():
    """Generate a cryptographically secure four-digit unlock PIN."""
    return 1000 + secrets.randbelow(9000)


def full_stations():
    """Return names of stations whose bike count equals their capacity."""
    stations = CONNECTION.execute("SELECT name FROM stations WHERE bikes = capacity").fetchall()
    return [station[0] for station in stations]   


def reset_station(station_id):
    """Empty a station, allowing database failures to reach the caller."""
    CONNECTION.execute(
        "UPDATE stations SET bikes = 0 WHERE id = ?", (station_id,)
    )


def has_bikes(station_id):
    """Return False for missing stations, NULL counts, or empty stations."""
    row = CONNECTION.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    return row is not None and row[0] is not None and row[0] > 0


def main():
    """Demonstrate registration, rental, PIN generation, and station reset."""
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)
    print(rent_bike(2), not rent_bike(9))
    print(unlock_pin(), full_stations(), has_bikes(2))
    reset_station(1)


if __name__ == "__main__":
    try:
        main()
    finally:
        CONNECTION.close()
