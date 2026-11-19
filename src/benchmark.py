"""PySpark vs Pandas: 3 queries x 3 runs x {25,50,100}% data; checks result agreement.
Run:  python src/benchmark.py
"""
import json, platform, time, os
import pandas as pd
from pyspark.sql import functions as F
from spark_pipeline import spark_session, SCHEMA
from config import *

RUNS, FRACS = 3, [0.25, 0.5, 1.0]
CSV = str(DATA / "station_hour.csv")

def pandas_queries(pdf):
    pdf = pdf.copy(); pdf["ts"] = pd.to_datetime(pdf["Datetime"]); pdf["month"] = pdf.ts.dt.month; pdf["hour"] = pdf.ts.dt.hour
    return {"q1_station_avg": pdf.groupby("StationId")["PM2.5"].mean(),
            "q2_month_avg": pdf.groupby("month")["PM2.5"].mean(),
            "q3_hour_bucket": pdf.groupby(["hour", "AQI_Bucket"]).size()}

def spark_queries(sdf):
    sdf = sdf.withColumn("ts", F.to_timestamp("Datetime")).withColumn("month", F.month("ts")).withColumn("hour", F.hour("ts"))
    return {"q1_station_avg": sdf.groupBy("StationId").agg(F.avg("`PM2.5`").alias("v")).toPandas(),
            "q2_month_avg": sdf.groupBy("month").agg(F.avg("`PM2.5`").alias("v")).toPandas(),
            "q3_hour_bucket": sdf.groupBy("hour", "AQI_Bucket").count().toPandas()}

def main():
    spark = spark_session()
    full_pd = pd.read_csv(CSV)
    full_sp = spark.read.csv(CSV, header=True, schema=SCHEMA).cache(); full_sp.count()
    rows = []
    for frac in FRACS:
        pdf = full_pd.sample(frac=frac, random_state=42) if frac < 1 else full_pd
        sdf = full_sp.sample(fraction=frac, seed=42) if frac < 1 else full_sp
        sdf = sdf.cache(); sdf.count()
        for r in range(RUNS):
            t = time.perf_counter(); pres = pandas_queries(pdf); tp = time.perf_counter() - t
            t = time.perf_counter(); sres = spark_queries(sdf); ts = time.perf_counter() - t
            rows.append({"fraction": frac, "run": r + 1, "rows": len(pdf), "pandas_s": tp, "spark_s": ts})
        sdf.unpersist()
    # correctness on the full data
    p = pandas_queries(full_pd)["q2_month_avg"].sort_index().values
    s = spark_queries(full_sp)["q2_month_avg"].sort_values("month")["v"].values
    df = pd.DataFrame(rows)
    summ = df.groupby("fraction").agg(rows=("rows", "first"), pandas_s=("pandas_s", "mean"), spark_s=("spark_s", "mean")).reset_index()
    summ["speedup"] = summ.pandas_s / summ.spark_s
    summ.to_csv(OUT / "benchmark.csv", index=False)
    env = {"cpu": platform.processor(), "cores": os.cpu_count(), "os": platform.platform(),
           "python": platform.python_version(), "spark": spark.version, "pandas": pd.__version__,
           "q2_max_abs_diff": float(abs(p - s).max())}
    json.dump(env, open(OUT / "benchmark_env.json", "w"), indent=2)
    print(summ.to_string(index=False)); print(env)
    spark.stop()

if __name__ == "__main__":
    main()
