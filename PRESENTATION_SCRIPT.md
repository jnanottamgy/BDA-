# Presentation Script: AirScope India
**Scalable Analysis of Hourly Air Quality Data from Indian Monitoring Stations Using Apache PySpark**
Presenters: **Jnanottam** (J) and **Harshavardha** (H) · Total time: about 10–12 minutes

> Before presenting: run the analysis on the real `city_hour.csv` and fill in every **[ ]** with the number shown on screen. Don't guess numbers.
> Have `app.html` open on the landing page, with the data already loaded in a second tab as a backup.

---

## Part 1: Introduction (Jnanottam, ~2 min)
*Screen: landing page, top of the page.*

**J:** Good morning, ma'am, and everyone. I'm Jnanottam, and this is Harshavardha. Our Big Data Analytics project is **"Scalable Analysis of Hourly Air Quality Data from Indian Monitoring Stations using Apache PySpark."** Our guide is Uzma Sultana ma'am.

**J:** Air pollution is one of India's biggest public-health problems. The Central Pollution Control Board, the CPCB, runs monitoring stations across the country. **Every hour**, each station records pollutants like PM2.5, PM10, NO₂, SO₂, CO and ozone.

**J:** Over five years, from 2015 to 2020, that adds up to about **2.6 million hourly records** from 26 cities. That's too much to handle comfortably in Excel or plain Python, which is why we treated it as a Big Data problem.

*Point to the coloured AQI bar.*

**J:** Throughout the project we use the official **CPCB AQI scale**: green is Good, then Satisfactory, Moderate, Poor, Very Poor, and dark red is Severe. Every chart you'll see is colour-coded with this scale, so you can tell how bad the air is at a glance.

*Scroll to "Six questions".*

**J:** We set out to answer six questions:
1. **When** is the air worst: which months, seasons and hours?
2. **Where** is it worst: which cities and stations?
3. How often is each city in Good vs Severe air?
4. Did the **2020 COVID lockdown** actually clean the air?
5. How **reliable** is the sensor data?
6. Is Big Data software like **PySpark faster** than a normal tool like Pandas?

**J:** Now Harshavardha will explain the data and how we processed it.

---

## Part 2: Data and pipeline (Harshavardha, ~2 min)
*Screen: scroll to "Pipeline" and "Research basis".*

**H:** Thank you. Our dataset is **"Air Quality Data in India 2015–2020"** from Kaggle. It's original CPCB data. It covers 12 pollutants plus the AQI value and AQI category for every hour.

**H:** In terms of the **V's of Big Data**:
- **Volume:** millions of rows.
- **Variety:** sensor readings plus station metadata.
- **Veracity:** a lot of missing values, because sensors fail.
- **Velocity:** new data arrives every hour, though we process it as a historical batch.

**H:** Our pipeline has five steps:
1. **Ingest:** read the CSV with a fixed schema.
2. **Clean:** remove duplicate readings, and blank out impossible values like negative or extremely high readings.
3. **Enrich:** join station names and cities, and add year, month, hour and season.
4. **Aggregate:** group the data and calculate averages using Spark SQL, and store the result in Parquet format.
5. **Insight:** charts, benchmarks and an AI summary.

**H:** Our base paper is **Bogomolov and Plotnikov, 2024**. They used PySpark on air-monitoring data and compared it with Pandas. We applied the same idea to **public Indian data**, with clearly documented cleaning rules, so anyone can reproduce our work.

**H:** The main processing is in **PySpark**. For this live demo, we built a dashboard that runs the same SQL logic directly in the browser. Let me open it.

*Click **Launch dashboard**, then **Load data**, then show the loaded file and the log.*

---

## Part 3: Overview and data quality (Jnanottam, ~1.5 min)
*Screen: **Overview**.*

**J:** This is the overview. Across all cities, the average PM2.5 is **[  ] µg/m³**, which falls in the **[  ]** category. Average PM10 is **[  ]**.

**J:** The key findings are on the right. The most polluted city is **[  ]**, and the cleanest is **[  ]**.

*Click **Data quality**.*

**J:** Before trusting any result, we checked the data quality. We started with **[  ]** raw records, removed **[  ]** duplicates and **[  ]** invalid rows, and kept **[  ]** clean records.

**J:** These bars show how complete each sensor is. Green is mostly complete and red is mostly missing. For example, PM2.5 is **[  ]%** complete, but some pollutants like **[  ]** are mostly missing. That's why we report missing data instead of hiding it.

---

## Part 4: Time patterns and cities (Harshavardha, ~2 min)
*Screen: **Time patterns**.*

**H:** First question: **when** is the air worst?

**H:** These four cards are the seasons. **Winter** is clearly the worst at **[  ]**, which is **[  ]**. **Monsoon** is the cleanest at **[  ]**. The reason is that in winter, cold air traps pollution near the ground and there is crop-residue burning, while monsoon rain washes particles out of the air.

**H:** The monthly chart shows the same wave every year: high in winter and low in monsoon. The red zone marks the 2020 lockdown, and you can see the drop there.

**H:** By hour of day, pollution peaks around **[  ]:00** and is lowest around **[  ]:00**. That's because the night-time air layer is shallow and traps pollution, and there is evening traffic.

*Click **Cities & AQI**.*

**H:** Second question: **where** is it worst? **[  ]** is the most polluted city and **[  ]** the cleanest, a difference of **[  ]×**. Most of the red and orange cities are in the Indo-Gangetic plain in North India.

**H:** The chart on the right shows what share of hours each city spends in each AQI category. You can see how rarely the most polluted cities have green, "Good" air.

---

## Part 5: Lockdown impact (Jnanottam, ~1.5 min)
*Screen: **Lockdown**.*

**J:** Our most interesting finding is the **COVID-19 lockdown**. We compared March–May 2020 with the same months in 2017 to 2019, so seasonal differences don't affect the comparison.

**J:** PM2.5 **fell [  ]%**, PM10 fell **[  ]%**, and NO₂, which mostly comes from vehicles, fell **[  ]%**.

**J:** Interestingly, **ozone rose [  ]%**. That matches the science: NO normally breaks ozone down, so with less traffic there is less NO, and ozone builds up.

**J:** On the right, green bars are cities that improved. This shows that when human activity stops, air quality improves quickly. That's a strong message for policymakers.

---

## Part 6: Performance (Harshavardha, ~1.5 min)
*Screen: **Performance**. Load `benchmark.csv` beforehand.*

**H:** The last question is about Big Data performance. We ran 3 queries, 3 times each, on 25%, 50% and 100% of the data, comparing **PySpark** with **Pandas** on the same laptop.

**H:** Our results: at full size, Pandas took **[  ]s** and PySpark took **[  ]s**, a speedup of **[  ]×**.

**H:** *(If PySpark was slower on small data:)* On smaller data, Spark can actually be slower, because starting it takes a few seconds. Spark's advantage shows up as data grows. On a multi-node cluster it would scale much further. The base paper reported the same trade-off.

**H:** We also checked **correctness**: Spark and Pandas gave the same averages, with a maximum difference of **[  ]**.

---

## Part 7: AI assistant and conclusion (Jnanottam and Harshavardha, ~1.5 min)
*Screen: **Ask AI**. Click "Summarise the 5 key findings".*

**J:** We also added an AI assistant that runs on a free language model. It reads **only our aggregated results**, never the raw data, and explains them in plain language. *(Let it answer and read one line.)*

**H:** To conclude:
- Pollution in India is strongly **seasonal**: winter is worst and monsoon is cleanest.
- **North Indian cities** are the most polluted.
- The **lockdown** showed that cutting emissions improves air quickly.
- **PySpark** let us process millions of records in a reproducible way.

**J:** Our limitations: we used a single machine, the sensor data has gaps, and the data ends in 2020. For future work, we'd like to run on a **multi-node cluster**, add newer data, and use **Spark MLlib to forecast PM2.5**.

**J & H:** Thank you. We're happy to take questions.

---

## Likely viva questions and short answers

| Question | Who answers | Answer |
|---|---|---|
| Why is this Big Data? | H | Millions of rows, many missing values, and it grows every hour. Spark processes it in parallel and scales to a cluster. |
| Why PySpark and not just Pandas? | H | Pandas is single-threaded and keeps everything in memory. Spark splits the work into partitions, uses all CPU cores, and can scale out to a cluster. |
| What is Parquet and why use it? | J | A columnar file format. It is compressed, and a query reads only the columns it needs, so it is much faster than CSV. |
| How did you handle missing values? | J | We didn't fill them with made-up numbers. Invalid values became null, rows with no PM reading were dropped, and we report completeness for each pollutant. |
| Why compare with 2017–19 instead of just Feb 2020? | J | Pollution is seasonal. Comparing the same months removes the season effect. |
| Why did ozone increase? | J | Less NO from traffic means less ozone gets broken down. This is the "titration" effect. |
| Why can Spark be slower on small data? | H | JVM start-up, task scheduling and shuffle overhead. It pays off only at large scale. |
| What does the in-browser dashboard use? | H | DuckDB-WASM, a columnar SQL engine running in the browser. It uses the same SQL logic as our Spark job, and it's for the demo only. |
| Is any data sent to the AI? | J | Only aggregated averages and counts, never raw rows. The API key stays in the browser. |
| What's your future scope? | J | A multi-node cluster, newer data, and PM2.5 forecasting with Spark MLlib. |
