# red-sox-offense-analysis
Python analysis of Boston Red Sox offensive performance across different portions of the 2024–2026 seasons, including comparisons with MLB-wide offensive trends.

# Boston Red Sox Offensive Performance by Season Period (2024–2026)

## Overview

This project analyzes whether the Boston Red Sox offense performed better during July and August than during the beginning and end of the season from 2024–2026.

Using Python, game-level data, and team batting statistics, each season is divided into three periods:

- **Early:** Opening Day through June 30
- **Middle:** July 1 through August 31
- **Late:** September 1 through the end of the regular season

Offensive performance is evaluated using runs per game, batting average (AVG), on-base percentage (OBP), slugging percentage (SLG), and OPS. Red Sox performance is also compared with MLB-wide offensive performance over the same periods.

## Key Findings

- The Red Sox recorded their highest runs per game and OPS during July and August in all three seasons analyzed.
- Across 2024–2026, Boston averaged **5.22 runs per game with a .773 OPS** during the Middle period.
- This compares with **4.44 runs per game and a .726 OPS** during the Early period and **3.72 runs per game and a .679 OPS** during the Late period.
- Boston's OPS was further above the MLB average during July and August than during the Early or Late periods in each of the three seasons.
- The results identify a consistent three-season pattern, but the sample is not sufficient to establish a long-term tendency.

## Tools

- Python
- pandas
- NumPy
- Matplotlib
- pybaseball
- Baseball-Reference
