# SE Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Problem Statement #24 — Smart Cities, Transport & Logistics**
**Public Bus Live Tracking & Crowding Estimator**

PES University, Dept. of Computer Science & Engineering
Name: Prajin Ravi Shankar | Roll No: PES1UG24CS082

## Overview

A municipal transit intelligence platform that ingests GPS feeds from city buses, estimates arrival times (ETA) at downstream stops, and computes passenger crowding levels from ticketing sensors.

**Actors:** Commuter, GPS Telemetry System, Ticketing Sensor System, Fleet Controller

## Contents

| File | Description |
|---|---|
| `Requirements_Table.docx` | 5 functional requirements (FR-001–FR-005) and 2 non-functional requirements (NFR-001–NFR-002), each with Req ID, Type, Description, Priority, Acceptance Criteria, and Rationale |
| `usecase_diagram.pdf` | UML use-case diagram — 4 actors, 7 use cases, 3 `<<include>>` relations, 1 `<<extend>>` relation |
| `UseCase_Flow.docx` | One-page use-case flow specification for UC-02 (View Bus Arrival & Crowding) — Preconditions, Postconditions, Main Success Scenario, Alternate Flow |

## Use Cases

- **UC-01** Search Route / Stop
- **UC-02** View Bus Arrival & Crowding — includes UC-03, UC-04
- **UC-03** Calculate ETA
- **UC-04** Estimate Crowding Level
- **UC-05** Ingest GPS Telemetry — includes UC-03
- **UC-06** Monitor Fleet Status
- **UC-07** Receive Delay Alert — extends UC-06

## Deliverable Requirements (per lab handout)

- [x] Requirements table — exactly 5 FRs, 2 NFRs, with measurable acceptance criteria
- [x] UML use-case diagram (PDF) with at least one `<<include>>` and one `<<extend>>`
- [x] Use-case flow document (one page) with Main Success Scenario and Alternate Flow
