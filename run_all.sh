#!/usr/bin/env bash
set -e; cd "$(dirname "$0")"
python src/spark_pipeline.py && python src/benchmark.py && python src/visualize.py
echo "Done. Open presentation/index.html"
