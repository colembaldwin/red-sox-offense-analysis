import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pybaseball import schedule_and_record, batting_stats_range
def calculate_batting_stats(data):
    """Calculate AVG, OBP, SLG, and OPS from batting data."""

    H = data["H"].sum()
    AB = data["AB"].sum()
    BB = data["BB"].sum()
    HBP = data["HBP"].sum()
    SF = data["SF"].sum()

    TB = (
        data["H"].sum()
        + data["2B"].sum()
        + 2 * data["3B"].sum()
        + 3 * data["HR"].sum()
    )

    AVG = H / AB
    OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
    SLG = TB / AB
    OPS = OBP + SLG

    return {
        "AVG": round(AVG, 3),
        "OBP": round(OBP, 3),
        "SLG": round(SLG, 3),
        "OPS": round(OPS, 3)
    }

def assign_period(date):
    """Assign a game date to the Early, Middle, or Late season period."""

    month = date.month

    if month <= 6:
        return "Early"
    elif month <= 8:
        return "Middle"
    else:
        return "Late"

  def calculate_runs_per_game(data):
    """Calculate average runs scored per game."""

    return round(data["R"].mean(), 2)

def prepare_schedule(data, year):
    """Clean schedule dates and assign each game to a season period."""

    data = data.copy()

    data["Date"] = data["Date"].str.replace(
        r" \(\d+\)", "", regex=True
    )

    data["Date"] = pd.to_datetime(
        data["Date"] + f" {year}",
        format="%A, %b %d %Y"
    )

    data["Period"] = data["Date"].apply(assign_period)

    return data

def analyze_red_sox_season(year, batting_file):
    """Calculate Red Sox offensive statistics by season period."""

    schedule = schedule_and_record(year, "BOS")
    schedule = prepare_schedule(schedule, year)

    batting = pd.read_csv(batting_file)

    batting_periods = {
        "Early": ["April/March", "May", "June"],
        "Middle": ["July", "August"],
        "Late": ["Sept/Oct"]
    }

    results = {}

    for period, splits in batting_periods.items():
        batting_data = batting[
            batting["Split"].isin(splits)
        ]

        stats = calculate_batting_stats(batting_data)

        schedule_data = schedule[
            schedule["Period"] == period
        ]

        stats["Runs Per Game"] = calculate_runs_per_game(schedule_data)

        results[period] = stats

    return results

def analyze_mlb_season(year, late_end_date):
    """Calculate MLB-wide offensive statistics by season period."""

    date_ranges = {
        "Early": (f"{year}-03-20", f"{year}-06-30"),
        "Middle": (f"{year}-07-01", f"{year}-08-31"),
        "Late": (f"{year}-09-01", late_end_date)
    }

    results = {}

    for period, (start_date, end_date) in date_ranges.items():
        batting = batting_stats_range(start_date, end_date)
        results[period] = calculate_batting_stats(batting)

    return results

Red_Sox_Offense_2024 = analyze_red_sox_season(
    2024,
    "BOS_2024.csv"
)

Red_Sox_Offense_2025 = analyze_red_sox_season(
    2025,
    "BOS_2025.csv"
)

Red_Sox_Offense_2026 = analyze_red_sox_season(
    2026,
    "BOS_2026.csv"
)

MLB_Offense_2024 = analyze_mlb_season(
    2024,
    "2024-10-31"
)

MLB_Offense_2025 = analyze_mlb_season(
    2025,
    "2025-10-31"
)

MLB_Offense_2026 = analyze_mlb_season(
    2026,
    "2026-10-01"
)

rows = []

for year, offense in [
    (2024, Red_Sox_Offense_2024),
    (2025, Red_Sox_Offense_2025),
    (2026, Red_Sox_Offense_2026)
]:
    for period in ["Early", "Middle", "Late"]:
        rows.append({
            "Year": year,
            "Period": period,
            "Runs Per Game": offense[period]["Runs Per Game"],
            "AVG": offense[period]["AVG"],
            "OBP": offense[period]["OBP"],
            "SLG": offense[period]["SLG"],
            "OPS": offense[period]["OPS"]
        })

RedSox_Offense_2024_2026 = pd.DataFrame(rows)

comparison_rows = []

for year, red_sox, mlb in [
    (2024, Red_Sox_Offense_2024, MLB_Offense_2024),
    (2025, Red_Sox_Offense_2025, MLB_Offense_2025),
    (2026, Red_Sox_Offense_2026, MLB_Offense_2026)
]:
    for period in ["Early", "Middle", "Late"]:
        comparison_rows.append({
            "Year": year,
            "Period": period,
            "Red Sox OPS": red_sox[period]["OPS"],
            "MLB OPS": mlb[period]["OPS"],
            "OPS Difference": round(
                red_sox[period]["OPS"] - mlb[period]["OPS"],
                3
            )
        })

Offense_Comparison = pd.DataFrame(comparison_rows)

Period_Averages = (
    RedSox_Offense_2024_2026
    .groupby("Period")[
        ["Runs Per Game", "AVG", "OBP", "SLG", "OPS"]
    ]
    .mean()
    .loc[["Early", "Middle", "Late"]]
    .round(3)
)

RedSox_2026_Case_Study = RedSox_Offense_2024_2026[
    RedSox_Offense_2024_2026["Year"] == 2026
].copy()

Wild_Card_Row = {
    "Year": 2026,
    "Period": "Wild Card Series",
    "Runs Per Game": 1.00,
    "AVG": 0.117,
    "OBP": 0.159,
    "SLG": 0.250,
    "OPS": 0.409
}

RedSox_2026_Case_Study.loc[
    len(RedSox_2026_Case_Study)
] = Wild_Card_Row

# Plot Red Sox runs per game by season period

periods = ["Early", "Middle", "Late"]
years = [2024, 2025, 2026]

x = np.arange(len(periods))
width = 0.25

for i, year in enumerate(years):
    data_year = RedSox_Offense_2024_2026[
        RedSox_Offense_2024_2026["Year"] == year
    ]

    data_year = data_year.set_index("Period").loc[periods]

    plt.bar(
        x + (i - 1) * width,
        data_year["Runs Per Game"],
        width,
        label=str(year)
    )

plt.xticks(x, periods)
plt.xlabel("Season Period")
plt.ylabel("Runs Per Game")
plt.title("Red Sox Runs Per Game by Season Period, 2024–2026")
plt.legend(title="Year")
plt.tight_layout()
plt.show()

# Plot Red Sox OPS difference from MLB average

x = np.arange(len(periods))
width = 0.25

for i, year in enumerate(years):
    data_year = Offense_Comparison[
        Offense_Comparison["Year"] == year
    ]

    data_year = data_year.set_index("Period").loc[periods]

    plt.bar(
        x + (i - 1) * width,
        data_year["OPS Difference"],
        width,
        label=str(year)
    )

plt.axhline(0, linewidth=1)
plt.xticks(x, periods)
plt.xlabel("Season Period")
plt.ylabel("Red Sox OPS - MLB OPS")
plt.title("Red Sox OPS Relative to MLB Average, 2024–2026")
plt.legend(title="Year")
plt.tight_layout()
plt.show()

# Plot 2026 regular-season periods and Wild Card Series OPS

plt.bar(
    RedSox_2026_Case_Study["Period"],
    RedSox_2026_Case_Study["OPS"]
)

plt.xlabel("Season Period")
plt.ylabel("OPS")
plt.title("Red Sox OPS by Season Period and Wild Card Series, 2026")
plt.tight_layout()
plt.show()

# Display analysis results

print("\nRed Sox Offensive Performance, 2024–2026")
print(RedSox_Offense_2024_2026.to_string(index=False))

print("\nThree-Year Period Averages")
print(Period_Averages)

print("\nRed Sox OPS Compared with MLB Average")
print(Offense_Comparison.to_string(index=False))

print("\n2026 Wild Card Series Case Study")
print(RedSox_2026_Case_Study.to_string(index=False))

