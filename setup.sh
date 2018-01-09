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

    zip -r ${zip_name} . >> /dev/null

    echo "Uploading zip $zip_name to S3"
    aws s3 cp ${zip_name} "s3://${BUCKET}/$LAMBDA_FOLDER" >> /dev/null

    echo "Updating function"
    aws lambda update-function-code --function-name ${function_name} \
    --s3-bucket ${BUCKET} \
    --s3-key "${LAMBDA_FOLDER}${zip_name}" >> /dev/null

    rm ${zip_name}

    cd ..
}

# add some dependencies
cd searcher
pip3 install twitter-application-only-auth -t . >> /dev/null
cd ..

for folder in "${!LAMBDAS[@]}"
do
    handle_lambda ${folder} ${LAMBDAS[$folder]}
done

# remove the downloaded dependencies
cd searcher
rm -r *application_only*
cd ..
