## Installation
If you're using uv
```bash
# Install dependencies and create virtual environment
uv sync

# Run game
uv run game/main.py
```
If you're not using uv
```bash
# Create a virtual environment (Unix/macOS)
python3 -m venv .venv
source .venv/bin/activate

# OR on Windows (cmd)
python -m venv .venv
.venv\Scripts\activate

# OR on Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run game
python3 game/main.py
```


## Problem Definition & Motivation 
- Quantum computing is still unefficient and not commonly applicable in modern systems
- We strive to utilize the unique properties of quantum computing through qiskit to demonstrate its capabilities
- To achieve this goal, we create an interactive game, visualizing the character and its interactions with the environment

## Inspirations
https://chetbae.github.io/quantum-pacman/

## Technical Approach (Theory)
Design a game leveraging quantum mechanism provided by the qiskit library
1. superposition: all walls are visible (for show) but are in a superposition of existence (some can be moved through, the real measurement is done when you touch them)
2. entanglement: all pixels for a wall (technically individual walls) that are adjacent to eachother are entangled so that their superposition leads to the same result when measured. also, the ghosts (and or particles) have their fates entangled (eating one has a chance to eat others)

## Implementation quality
- Aiming for clean, readable and functioning program

## Result & Evaluation
- Collect histograms or other graphs of quantum vs classical runs
- Visualize the stats/noise and give a demo of the game

## Quantum Rigor & Insight
- Illustrate the connection between quantum properties with our interactive demo

## Reproducibility & Repo Quality
- Readme contains all details to run

## Impact & Creativity
- Educates users of quantum peroperties such as superposition and entanglement
- Built using quantum library

## Teamwork & Process
Daniel: 
<br>
Waaberi:
<br>
Samith:
<br>
Aarya:
<br>

## External Contributors
ChatGPT
<br>
Claude

## Ideas:
- Entanglement
- Superposition