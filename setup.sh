#!/usr/bin/env bash

declare -A LAMBDAS=(["searcher"]="TwitterSearcher" ["email"]="MailSenderLambda" ["speech"]="TextToSpeechLambda")

BUCKET="lambdas-sam-van-overmeire"
LAMBDA_FOLDER="lambda-zips/"
LAMBDA_NAME="TwitterSearcher"

function handle_lambda {
    folder=$1
    function_name=$2
    zip_name=${folder}.zip

    cd ${folder}

    pip3 install -r requirements.txt -t . >> /dev/null

    zip -r ${zip_name} . >> /dev/null

    echo "Uploading zip $zip_name to S3"
    aws s3 cp ${zip_name} "s3://${BUCKET}/$LAMBDA_FOLDER" >> /dev/null

    echo "Updating function"
    aws lambda update-function-code --function-name ${function_name} \
    --s3-bucket ${BUCKET} \
    --s3-key "${LAMBDA_FOLDER}${zip_name}" >> /dev/null

    # remove anything that isn't a python script or requirements.txt
    ls | grep -v "\.py\|requirements\.txt" | xargs -I{} rm -r {}

    cd ..
}

for folder in "${!LAMBDAS[@]}"
do
    handle_lambda ${folder} ${LAMBDAS[$folder]}
done
