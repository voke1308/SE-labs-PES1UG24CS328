# SE Lab 3: Component Modelling & Architectural Pattern Selection

**Course:** Software Engineering (UE24CS341A)  
**Student Name:** Prajin Ravi Shankar  
**SRN:** PES1UG24CS328  
**Section / Roll No:** 5-F  
**Assigned Problem Statement:** #24 — Public Bus Live Tracking & Crowding Estimator System  

---

##  Problem Overview
A municipal transit intelligence platform ingesting GPS feeds from city buses, estimating arrival times (ETA) at downstream stops, and computing passenger crowding levels from ticketing sensors.

**Primary Actors:**
* Commuter
* Fleet Controller

---

##  Architectural Selection
**Selected Pattern:** Microservices Architecture (with Asynchronous Event Messaging)

### **Key System Components**
1. **`Commuter API Component`**: Manages commuter search requests for routes/stops and serves live location/crowding data.
2. **`GPS & Sensor Ingestion Component`**: Handles high-frequency GPS telemetry streams (every 5 seconds) and ticketing sensor updates.
3. **`Tracking & ETA Service Component`**: Processes telemetry data to compute live arrival ETAs for upcoming route stops.
4. **`Crowding Estimator Component`**: Evaluates passenger boarding and alighting counts to assign crowding levels (Low / Medium / High).
5. **`Fleet Monitoring & Alert Component`**: Tracks schedule delays and triggers alerts to the Fleet Controller when deviations exceed 5 minutes.
6. **`Database Component`**: Manages persistent storage and historical logging of trip positions and crowding records for 30 days.

---

##  Component Diagram

Below is the UML Component Diagram modeled using standard ball-and-socket (lollipop/assembly) interface notation.

```plantuml
@startuml
skinparam componentStyle uml2
skinparam Monochrome true
skinparam FrameBackgroundColor white
skinparam BackgroundColor white

package "Public Bus Live Tracking & Crowding Estimator System" {

  [Commuter API Component] as Commuter
  [GPS & Sensor Ingestion Component] as Ingestion
  [Tracking & ETA Service Component] as Tracking
  [Crowding Estimator Component] as Crowding
  [Fleet Monitoring & Alert Component] as Fleet
  [Database Component] as DB

  ' Provided Interfaces (Lollipops / Circles)
  () ICommuterSearchService
  () ITelemetryIngestionService
  () ICrowdingEstimationService
  () IDataPersistence

  ' Layout & Connections
  Commuter ..> ICommuterSearchService : <<use>>
  ICommuterSearchService - [Ingestion]

  Ingestion ..> ITelemetryIngestionService : <<use>>
  ITelemetryIngestionService - [Tracking]

  Tracking -( ICrowdingEstimationService : use
  ICrowdingEstimationService - [Crowding]

  [Crowding] - [Fleet]
  Fleet ..> IDataPersistence : <<use>>
  IDataPersistence - [DB]

}
@enduml
