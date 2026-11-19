"""Build charts from output/*.csv.  Run: python src/visualize.py"""
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from config import *
sns.set_theme(style="whitegrid"); CHARTS.mkdir(parents=True, exist_ok=True)
def save(name): plt.tight_layout(); plt.savefig(CHARTS / f"{name}.png", dpi=160); plt.close()

m = pd.read_csv(OUT / "monthly.csv"); m["date"] = pd.to_datetime(dict(year=m.year, month=m.month, day=1))
plt.figure(figsize=(11, 4)); plt.plot(m.date, m.pm25, label="PM2.5"); plt.plot(m.date, m.pm10, label="PM10", alpha=.7)
plt.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-05-31"), color="red", alpha=.12, label="Lockdown")
plt.ylabel("µg/m³"); plt.title("Monthly average particulate matter"); plt.legend(); save("01_monthly_trend")

h = pd.read_csv(OUT / "hourly.csv")
plt.figure(figsize=(9, 4)); sns.lineplot(data=h, x="hour", y="pm25", marker="o", label="PM2.5"); sns.lineplot(data=h, x="hour", y="pm10", marker="o", label="PM10")
plt.xticks(range(0, 24, 2)); plt.ylabel("µg/m³"); plt.title("Average pollution by hour of day"); save("02_hour_of_day")

s = pd.read_csv(OUT / "season.csv").set_index("season").loc[["Winter", "Summer", "Monsoon", "Post-monsoon"]]
s.plot.bar(figsize=(7, 4), rot=0); plt.ylabel("µg/m³"); plt.title("Seasonal averages"); save("03_season")

c = pd.read_csv(OUT / "city.csv").dropna(subset=["pm25"])
tb = pd.concat([c.head(8).assign(g="Most polluted"), c.tail(8).assign(g="Least polluted")])
plt.figure(figsize=(9, 6)); sns.barplot(data=tb, y="City", x="pm25", hue="g", dodge=False, palette=["#c0392b", "#27ae60"])
plt.xlabel("Mean PM2.5 (µg/m³)"); plt.title("Top & bottom cities"); plt.legend(title=""); save("04_cities")

a = pd.read_csv(OUT / "aqi_bucket.csv"); a = a.groupby(["City", "AQI_Bucket"])["count"].sum().unstack().reindex(columns=AQI_ORDER).fillna(0)
a = a.div(a.sum(1), axis=0).sort_values("Good")
a.plot.barh(stacked=True, figsize=(10, 8), color=["#2ecc71", "#a3d977", "#f1c40f", "#e67e22", "#e74c3c", "#8e1b1b"], width=.85)
plt.xlabel("Share of hours"); plt.title("AQI category distribution by city"); plt.legend(bbox_to_anchor=(1, 1)); save("05_aqi_distribution")

l = pd.read_csv(OUT / "lockdown.csv"); avg = l.groupby("period")[["pm25", "pm10", "no2", "co", "o3"]].mean().T
avg["change_%"] = (avg["2020"] / avg["2017-2019"] - 1) * 100; avg.to_csv(OUT / "lockdown_summary.csv")
avg[["2017-2019", "2020"]].plot.bar(figsize=(8, 4), rot=0, color=["#7f8c8d", "#2980b9"])
for i, v in enumerate(avg["change_%"]): plt.text(i, max(avg.iloc[i, :2]) * 1.02, f"{v:+.0f}%", ha="center", fontweight="bold")
plt.title("Mar–May: 2020 lockdown vs 2017–2019"); save("06_lockdown")

b = pd.read_csv(OUT / "benchmark.csv")
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(b.rows, b.pandas_s, "o-", label="Pandas"); ax[0].plot(b.rows, b.spark_s, "o-", label="PySpark"); ax[0].set(xlabel="Rows", ylabel="Seconds (mean of 3)", title="Runtime vs data size"); ax[0].legend()
ax[1].bar([f"{int(f*100)}%" for f in b.fraction], b.speedup, color="#8e44ad"); ax[1].axhline(1, ls="--", c="k"); ax[1].set(title="Speedup = Pandas ÷ PySpark")
save("07_benchmark")
print("Charts written to", CHARTS)
