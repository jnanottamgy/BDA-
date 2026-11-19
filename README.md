# Scalable Analysis of Hourly Indian Air Quality Data with PySpark
CSE557 Big Data Analytics, RIT · Harshavardha Satish Kumar (1MS24CS065) · Guide: Uzma Sultana

## Setup
1. Install Python 3.10–3.12 and Java 17, then run `pip install -r requirements.txt`
2. Download the Kaggle dataset **rohanrao/air-quality-data-in-india** and copy `station_hour.csv` and `stations.csv` into `data/`
3. Run `./run_all.sh` (or each script in `src/` in order)
4. Open `presentation/index.html` in a browser. Use the arrow keys to move between slides.

## Layout
| File | Purpose |
|---|---|
| `src/spark_pipeline.py` | Loads data with an explicit schema, cleans it (duplicates, ranges, station join), adds time features, writes Parquet, runs the 7 analyses |
| `src/benchmark.py` | Pandas vs PySpark: 3 queries × 3 runs × 25/50/100% data, speedup, correctness check, hardware log |
| `src/visualize.py` | Draws 7 charts into `output/charts/` |
| `presentation/index.html` | 14-slide deck that pulls in the charts |

## Outputs
`output/data_quality.json`, `monthly/hourly/season/city/station/aqi_bucket/lockdown.csv`, `lockdown_summary.csv`, `benchmark.csv`, `benchmark_env.json`, and the charts.

**Google Colab:** upload the repo, `!pip install pyspark`, then `!bash run_all.sh`.
