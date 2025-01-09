#! /bin/bash

set -e

TODAY=$(date +%Y-%m-%d)
echo "Running digital land builder on $TODAY"

if [ -z "$READ_S3_BUCKET" ]; then
    echo READ_S3_BUCKET not set so files will be downloaded from the production files cdn
fi

if [ -z "$WRITE_S3_BUCKET" ]; then
    echo WRITE_S3_BUCKET not set so files will not be uploaded to an S3 Bucket
fi

# Setup
make makerules
make init

# Run
make

# TODO: push the resulting files back to S3
