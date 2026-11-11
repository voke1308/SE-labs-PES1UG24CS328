# Lab 5: Static Code Analysis

Student identifier: PES1UG24CS328.

Assignment source:
https://github.com/SETAPESU26/L5_23_bike_share_stations

## Deliverables

- `bike_share_stations.py`: corrected program.
- `issues.md`: findings, original line references, and fixes.
- `reports/before/` and `reports/after/`: genuine Pylint, Bandit, Flake8, and demonstration outputs.
- `reports/verification.txt`: regression-test results.
- `original/bike_share_stations.py`: unchanged starter for comparison.
- `ASSIGNMENT_README.md`: upstream assignment instructions.
- `test_bike_share_stations.py`: ten regression checks.
- `requirements-dev.txt` and `analyze.py`: tools and repeatable report generation.
- `stages/`: snapshots of the three analysis stages.

The reflection answers were removed after instructor clarification, as recorded in [commit `511b43c`](https://github.com/voke1308/SE-labs-PES1UG24CS328/commit/511b43c150bdc10891311de3d4cd724630218930).

## Results

On Python 3.12.14, Pylint 4.1.3, Bandit 1.9.4, and Flake8 7.4.1:

| Check | Before | After |
|---|---|---|
| Pylint | 3.89/10; 22 messages | 10.00/10; no messages |
| Bandit | 3 findings: 1 medium, 2 low | No findings |
| Flake8 | 10 findings | No findings |
| Regression tests | Not applied to incompatible starter API | 10 passed |

No checks were disabled, no findings were suppressed, and no permissive lint configuration was added. The empty final Flake8 report is expected: successful Flake8 runs print nothing. See `reports/analysis_summary.json` for exit codes.

## Run locally

From this `lab5` directory with Python installed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe bike_share_stations.py
.\.venv\Scripts\python.exe -m unittest -v test_bike_share_stations
.\.venv\Scripts\python.exe analyze.py
```

`analyze.py` reruns both versions and overwrites their reports. PIN output and timestamps naturally differ between runs. The baseline tools return nonzero statuses because they find issues; this is expected.

## Behavior and scope

Station registration, bike rental, four-digit PIN generation, full-station listing, and station reset remain available. Functions now use snake_case names. `rent_bike` consistently returns a Boolean, including False for missing/empty stations; the demo was updated accordingly. `has_bikes` handles missing stations and NULL counts. Errors during reset now propagate to callers. The module does not execute its demo when imported.

Storage remains in memory, matching the assignment. This is a lab program; it does not implement a complete PIN authentication system or persistent storage. Secure randomness alone does not provide rate limiting or PIN expiry.

## Three-commit requirement

The three tool-specific fixes are in the repository history:

1. [Bandit fixes](https://github.com/voke1308/SE-labs-PES1UG24CS328/commit/47f2cbb60cecf6355b0822e8dd98aa98b8eeaa8e). Snapshot: `stages/01_bandit.py`.
2. [Pylint fixes](https://github.com/voke1308/SE-labs-PES1UG24CS328/commit/165c94be7a0d948d71ecf619186c0afbf4f7b100). Snapshot: `stages/02_pylint.py`.
3. [Flake8 fixes](https://github.com/voke1308/SE-labs-PES1UG24CS328/commit/48b7e3f1c485739e8f3718034ddecb311b776280). Snapshot: `stages/03_flake8.py`.

These files are historical snapshots, not additional production modules. Analyze the specific corrected file, not the complete archive recursively: `original/` and early `stages/` intentionally retain baseline findings.
