#!/bin/bash

set -e

ENTRY_DATE=$(date +%Y-%m-%d)
echo "Build digital-land-builder for entry date: $ENTRY_DATE"

DB=dataset/digital-land.sqlite3
DB_PERF=dataset/performance.sqlite3

if [ -z "$PARQUET_DIR" ]; then
  PARQUET_DIR="data/"
fi

# Set default PARQUET_SPECIFICATION_DIR if not set
if [ -z "$PARQUET_SPECIFICATION_DIR" ]; then
  export PARQUET_SPECIFICATION_DIR="${PARQUET_DIR}specification/"
fi

# Set default PARQUET_PERFORMANCE_DIR if not set
if [ -z "$PARQUET_PERFORMANCE_DIR" ]; then
  export PARQUET_PERFORMANCE_DIR="${PARQUET_DIR}performance/"
fi

if [ -z "$COLLECTION_DATASET_BUCKET_NAME" ]; then
    echo "$COLLECTION_DATASET_BUCKET_NAME"
    echo "assign value to COLLECTION_DATASET_BUCKET_NAME to save to a bucket" 
fi

echo Update makerules
make makerules

echo Install dependencies
make init

echo Clobber dataset
make clobber

mkdir -p dataset/

echo ">> First pass: downloading and concatenating data"
mkdir -p dataset/
./bin/download-collection.sh
./bin/download-pipeline.sh
./bin/concat.sh
python3 bin/download_issues.py
./bin/download-operational-issues.sh
python3 bin/download_column_field.py
python3 bin/download_converted_resources.py
python3 ./bin/concat-issues.py
python3 ./bin/concat-column-field.py
python3 ./bin/concat-converted-resource.py
python3 bin/download_expectations.py


echo ">> Second pass: generating $DB"
rm -f "$DB"
mkdir -p "$PARQUET_SPECIFICATION_DIR"
python3 bin/load.py "$DB"

echo ">> Third pass: generating $DB_PERF"
./bin/download-digital-land.sh
rm -f "$DB_PERF"
mkdir -p "$PARQUET_PERFORMANCE_DIR"
python3 bin/load_reporting_tables.py "$DB_PERF" "$DB"
python3 bin/load_performance.py "$DB_PERF" "$DB"

echo Check performance database
make check-performance

if [ -n "$COLLECTION_DATASET_BUCKET_NAME" ]; then
    echo Save datasets to $COLLECTION_DATASET_BUCKET_NAME
    make save-dataset
else
    echo "No COLLECTION_DATASET_BUCKET_NAME defined so dataset files not pushed to s3"
fi

if [ -n "$COLLECTION_DATASET_BUCKET_NAME" ]; then
    echo Save Parquet files to $COLLECTION_DATASET_BUCKET_NAME
    make save-tables-to-parquet
else
    echo "No COLLECTION_DATASET_BUCKET_NAME defined so parquet files not pushed to s3"
fi

echo "Digital Land build complete"


