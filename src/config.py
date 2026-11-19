"""Shared paths and constants."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"            # put station_hour.csv, stations.csv, city_hour.csv here
OUT = ROOT / "output"
CHARTS = OUT / "charts"
PARQUET = OUT / "clean_parquet"
POLLUTANTS = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3",
              "Benzene", "Toluene", "Xylene"]
# Plausible physical ranges (µg/m3; CO in mg/m3) used for validation
VALID_RANGE = {p: (0, 1000) for p in POLLUTANTS} | {"PM10": (0, 2000), "CO": (0, 200)}
AQI_ORDER = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
SEASON = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Summer", 4: "Summer", 5: "Summer",
          6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon", 10: "Post-monsoon", 11: "Post-monsoon"}
LOCKDOWN_MONTHS = [3, 4, 5]
