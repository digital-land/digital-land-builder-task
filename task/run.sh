#! /bin/bash

set -e

TODAY=$(date +%Y-%m-%d)
echo "Running digital land builder on $TODAY"

if [ -z "$READ_S3_BUCKET" ]; then
    echo READ_S3_BUCKET not set so files will be downloaded from the production files CDN
fi

if [ -z "$WRITE_S3_BUCKET" ]; then
    echo WRITE_S3_BUCKET not set so files will not be uploaded to an S3 Bucket
fi

# Setup
make makerules
make init

# Make Digital Land DB
make clobber
make

# Make Performance DB
if [ "$BUILD_PERFOMANCE_DB" = "True" ]; then
    make clobber-performance
    make third-pass
fi


# Save the output to S3
if [ -n "$WRITE_S3_BUCKET" ]; then
    HOISTED_COLLECTION_DATASET_BUCKET_NAME=$WRITE_S3_BUCKET
    COLLECTION_DATASET_BUCKET_NAME=$WRITE_S3_BUCKET
    export HOISTED_COLLECTION_DATASET_BUCKET_NAME
    export COLLECTION_DATASET_BUCKET_NAME
    make save-dataset
else
    echo WRITE_S3_BUCKET not set so files not uploaded to S3
fi
