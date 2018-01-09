#!/usr/bin/env bash

SEARCHER_ZIP="searcher.zip"
BUCKET="lambdas-sam-van-overmeire"
LAMBDA_FOLDER="lambda-zips/"
LAMBDA_NAME="TwitterSearcher"

cd searcher
echo "Installing dependencies for searcher"
pip3 install twitter-application-only-auth -t . >> /dev/null

echo "Zipping"
zip -r ${SEARCHER_ZIP} . >> /dev/null

echo "Uploading zip to S3"
aws s3 cp ${SEARCHER_ZIP} "s3://${BUCKET}/$LAMBDA_FOLDER" >> /dev/null

echo "Updating function"
aws lambda update-function-code --function-name ${LAMBDA_NAME} \
    --s3-bucket ${BUCKET} \
    --s3-key "${LAMBDA_FOLDER}${SEARCHER_ZIP}" >> /dev/null

echo "Cleaning"
rm -r *application_only*
rm ${SEARCHER_ZIP}
