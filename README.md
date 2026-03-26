# 🧠 Smart Route Finder using A* Algorithm

## 📌 Overview
This project is an interactive visualization of the A* (A-Star) pathfinding algorithm, inspired by real-world navigation systems like Google Maps. It demonstrates how the shortest path is calculated between two points in the presence of obstacles.

---

## 🎯 Features
- Interactive grid-based map
- Start and end node selection
- Obstacle placement (blocked roads)
- Real-time A* pathfinding visualization
- Color-coded algorithm steps:
  - 🟠 Open nodes (being explored)
  - 🟣 Closed nodes (visited)
  - 🔵 Final shortest path
- Reset functionality (press **C**)

---

## 🧠 Algorithm Used

The A* algorithm uses the cost function:

f(n) = g(n) + h(n)

- **g(n)** → Actual cost from the start node  
- **h(n)** → Heuristic estimate to the goal (Manhattan distance)  
- **f(n)** → Total estimated cost  

This helps the algorithm efficiently find the shortest path.

---

## 🛠️ Tech Stack
- Python  
- Pygame  

---

## ▶️ How to Run

1. Make sure Python 3.11 is installed  
2. Install pygame:

```bash
pip install pygame
