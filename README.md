<p align="center">
  <img src="fig1.png" alt="Passing Network Example" width="700"/>
</p>

# UEFA Women's Euro 2025 Passing Network Visualization

This project provides a clear, reproducible workflow for visualizing football passing networks using open StatsBomb data, with a focus on the UEFA Women's Euro 2025. The main goal is to generate insightful, publication-quality passing network diagrams for any match in the dataset, using a modular and minimalistic approach.

## What We Do

- **Data Access:** We use the `statsbombpy` library to access open StatsBomb event data for UEFA Women's Euro 2025 matches.
- **Passing Network Calculation:** The code extracts starting XIs, computes average player positions, and builds passing matrices for each team, focusing on completed passes between starting players.
- **Visualization:** Using `mplsoccer` and `matplotlib`, we plot side-by-side passing networks for both teams, with node sizes and edge widths scaled to reflect pass volume. The layout and legend are designed for clarity and easy comparison.
- **Templates:** The project is structured with two main templates:
  - One for the plot layout (figure arrangement, legends, branding, etc.)
  - One for the passing network calculations (data wrangling, matrix building, scaling).
- **Branding:** The central logo and clean design make the plots suitable for presentations and publications.

## How to Use

1. **Install Requirements:**  
	Install dependencies from `requirements.txt` (see the relevant folder).
2. **Run the Script:**  
	Edit the parameters at the top of the main script to select your match, then run the script to generate the plot.
3. **Customize:**  
	Adjust the templates to analyze different matches or competitions as needed.

---
# Women_Euro_2025_Passing_Network