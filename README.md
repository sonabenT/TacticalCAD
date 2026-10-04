# TacticalCAD 
**Emergency Dispatch & Tactical Command System**

TacticalCAD is an interactive, browser-based Computer-Aided Dispatch (CAD) system engineered to simulate real-time emergency vehicle routing, dynamic traffic obstacle avoidance, and live mission telemetry tracking.

---

##  Key Features

* **Real-Time Dynamic Routing:** Uses a client-side implementation of Dijkstra's Algorithm to calculate the optimal path between dispatch base stations and incident locations.
* **Live Road Closure Simulation:** Interactively toggle specific road obstacles (e.g., flyovers, crossings) to force instant, real-time path recalculation.
* **GIS Map Integration:** Interactive map interface powered by Leaflet.js and OpenStreetMap tiles.
* **Live Telemetry:** Tracks turn-by-turn navigation paths, estimated travel distance, and active dispatch status.
* **Zero Backend Dependency:** Built as a pure client-side Single Page Application (SPA)—no API keys, database servers, or external backends required.

---

##  Tech Stack

* **Frontend:** HTML5, Tailwind CSS
* **Mapping Engine:** Leaflet.js (OpenStreetMap)
* **Algorithmic Core:** JavaScript (Custom Dijkstra's Algorithm)

---

##  How to Run

1. Clone or download this repository.
2. Open `index.html` directly in any web browser (or use VS Code Live Server).