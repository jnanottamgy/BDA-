"""PySpark pipeline: ingest -> clean -> feature -> analyse -> save results.
Run:  python src/spark_pipeline.py
"""
import json, time
from pyspark.sql import SparkSession, functions as F, types as T
from config import *

def spark_session():
    return (SparkSession.builder.appName("CPCB-AirQuality").master("local[*]")
            .config("spark.sql.shuffle.partitions", "16")
            .config("spark.driver.memory", "4g").getOrCreate())

SCHEMA = T.StructType([T.StructField("StationId", T.StringType()),
                       T.StructField("Datetime", T.StringType())] +
                      [T.StructField(p, T.DoubleType()) for p in POLLUTANTS] +
                      [T.StructField("AQI", T.DoubleType()), T.StructField("AQI_Bucket", T.StringType())])

def ingest(spark):
    hourly = spark.read.csv(str(DATA / "station_hour.csv"), header=True, schema=SCHEMA)
    stations = spark.read.csv(str(DATA / "stations.csv"), header=True, inferSchema=True)
    return hourly, stations

def quality_report(df):
    total = df.count()
    comp = df.select([(F.count(F.col(f"`{c}`")) / F.lit(total) * 100).alias(c) for c in POLLUTANTS + ["AQI"]]).first().asDict()
    return total, {k: round(v, 2) for k, v in comp.items()}

def clean(hourly, stations):
    raw_n = hourly.count()
    df = hourly.dropDuplicates(["StationId", "Datetime"])
    dup_removed = raw_n - df.count()
    df = df.withColumn("ts", F.to_timestamp("Datetime", "yyyy-MM-dd HH:mm:ss")).filter(F.col("ts").isNotNull())
    for p in POLLUTANTS:                         # out-of-range -> null (not dropped)
        lo, hi = VALID_RANGE[p]
        df = df.withColumn(p, F.when(F.col(f"`{p}`").between(lo, hi), F.col(f"`{p}`")))
    df = df.filter(F.col("`PM2.5`").isNotNull() | F.col("PM10").isNotNull())   # keep rows with a PM reading
    df = df.join(F.broadcast(stations.select("StationId", "StationName", "City", "State")), "StationId", "left")
    season = F.create_map([F.lit(x) for kv in SEASON.items() for x in kv])
    df = (df.withColumn("year", F.year("ts")).withColumn("month", F.month("ts"))
            .withColumn("hour", F.hour("ts")).withColumn("season", season[F.col("month")]))
    return df, raw_n, dup_removed

def analyse(df, spark):
    df.createOrReplaceTempView("aq")
    q = {}
    q["monthly"] = spark.sql("""SELECT year, month, AVG(`PM2.5`) pm25, AVG(PM10) pm10
                                FROM aq GROUP BY year, month ORDER BY year, month""")
    q["hourly"] = spark.sql("SELECT hour, AVG(`PM2.5`) pm25, AVG(PM10) pm10 FROM aq GROUP BY hour ORDER BY hour")
    q["season"] = df.groupBy("season").agg(F.avg("`PM2.5`").alias("pm25"), F.avg("PM10").alias("pm10"))
    q["city"] = (df.groupBy("City").agg(F.avg("`PM2.5`").alias("pm25"), F.count("*").alias("n"))
                   .filter("n > 1000").orderBy(F.desc("pm25")))
    q["station"] = (df.groupBy("StationName", "City").agg(F.avg("`PM2.5`").alias("pm25"), F.count("*").alias("n"))
                      .filter("n > 1000").orderBy(F.desc("pm25")).limit(15))
    q["aqi_bucket"] = (df.filter(F.col("AQI_Bucket").isNotNull())
                         .groupBy("City", "year", "AQI_Bucket").count())
    q["lockdown"] = spark.sql(f"""SELECT City, CASE WHEN year=2020 THEN '2020' ELSE '2017-2019' END period,
                                  AVG(`PM2.5`) pm25, AVG(PM10) pm10, AVG(NO2) no2, AVG(CO) co, AVG(O3) o3
                                  FROM aq WHERE month IN (3,4,5) AND year BETWEEN 2017 AND 2020
                                  GROUP BY City, period""")
    return {k: v.toPandas() for k, v in q.items()}

def main():
    spark = spark_session(); t0 = time.time()
    hourly, stations = ingest(spark)
    raw_total, raw_comp = quality_report(hourly)
    df, raw_n, dups = clean(hourly, stations)
    df.write.mode("overwrite").partitionBy("year").parquet(str(PARQUET))
    df = spark.read.parquet(str(PARQUET)).cache()
    clean_n = df.count()
    results = analyse(df, spark)
    OUT.mkdir(exist_ok=True)
    for k, v in results.items():
        v.to_csv(OUT / f"{k}.csv", index=False)
    json.dump({"raw_records": raw_n, "duplicates_removed": dups, "clean_records": clean_n,
               "completeness_pct_raw": raw_comp, "pipeline_seconds": round(time.time() - t0, 1)},
              open(OUT / "data_quality.json", "w"), indent=2)
    print(open(OUT / "data_quality.json").read())
    spark.stop()

if __name__ == "__main__":
    main()
