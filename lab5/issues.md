# Identified issues and fixes

Line numbers refer to `original/bike_share_stations.py`. Bandit severities below are the tool's actual values. Pylint/Flake8 findings have categories rather than Bandit-style security severities. No high-severity Bandit issues were reported.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Bandit B608 | Security - Medium | 9 | Station values are concatenated into SQL, allowing station names to change the query and breaking names with apostrophes. | Bind name, capacity, and bikes using SQLite `?` placeholders. |
| Bandit B311 | Security - Low | 22 | `random.randint` is unsuitable for an unlock PIN because it uses a non-cryptographic generator. | Use `1000 + secrets.randbelow(9000)` to preserve the four-digit range. |
| Bandit B110 / Pylint W0718 | Error handling - Low security / warning | 32-35 | A broad `except Exception: pass` hides reset failures and reports no useful error. | Remove the catch so database failures propagate to the caller. |
| Pylint W0102 | Correctness - warning | 8 | `log=[]` creates one shared list, leaking station names between independent calls. | Default to `None` and create a new list per call; preserve explicitly supplied lists. |
| Pylint R1710 | Correctness - refactor | 14-18 | Successful rentals return True but failures implicitly return None. | Use a conditional UPDATE and return `cursor.rowcount == 1`; update the demo to test a Boolean result. This also avoids a separate read/update sequence. |
| Pylint W0612 / Flake8 F841 | Maintainability - warning | 27 | `summary` is computed but never used. | Remove the unused variable. |
| Pylint C0121 / Flake8 E711 | Convention / style | 40 | Equality comparison to None should use an identity check. | Use `is not None` guards before inspecting the bike count. |
| Pylint C0103 | Naming convention | 8, 14, 21, 25, 31, 38 | Camel-case function names violate Python naming conventions. | Rename functions and every demo call to snake_case. |
| Pylint C0114 / C0116 | Documentation convention | 1, 8, 14, 21, 25, 31, 38, 45 | Module and functions lack docstrings. | Add concise purpose, return-behavior, and error-handling documentation. |
| Pylint C0301 / Flake8 E501 | Formatting | 5, 9, 15, 17, 26, 33, 39 | Long lines impair readability and exceed the style limit. | Wrap SQL and arguments inside parentheses; final code meets Flake8's default 79-character limit. |
| Pylint C0303 / Flake8 W291 | Formatting | 27 | Trailing spaces are present. | Remove trailing whitespace. |

## Additional manual findings

These were found during code inspection and behavioral testing, not claimed as tool findings:

- Original line 40 indexes a missing database row, raising TypeError. `has_bikes` now returns False when `fetchone()` returns None.
- Original line 53 runs the demo at import time. A `__name__` guard now prevents that; script execution closes the database in a finally block.

All three baseline Bandit issues were removed. Final reports confirm Pylint 10.00/10, no Bandit findings, and no Flake8 findings. The SQL-like station-name test, independent-log tests, rental boundary tests, PIN boundary tests, missing/NULL station checks, reset/error checks, and import test cover the changed behavior.
