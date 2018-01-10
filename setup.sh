#!/usr/bin/env bash

LAMBDAS=("searcher" "mail" "speech")

BUCKET="lambdas-sam-van-overmeire"
LAMBDA_FOLDER="lambda-zips/"
CLOUDFORMATION_FOLDER="cloudformation/"

SAM_YAML="sam-infra.yaml"
SAM_STACK_NAME="twitter-searcher-stack"

# gather requirements and upload zip; folders should be given as args
function handle_lambda {
    folder=$1
    zip_name=${folder}.zip

    cd ${folder}

    pip3 install -r requirements.txt -t . >> /dev/null
    zip -r ${zip_name} . >> /dev/null

    echo "Uploading zip $zip_name to S3"
    aws s3 cp ${zip_name} "s3://${BUCKET}/$LAMBDA_FOLDER" >> /dev/null

    # optional: remove anything that isn't a python script or requirements.txt
    ls | grep -v "\.py\|requirements\.txt" | xargs -I{} rm -r {}

    cd ..
}

for folder in "${LAMBDAS[@]}"
do
    handle_lambda ${folder}
done

echo "Deploying stack"
aws cloudformation deploy \
    --template-file ${SAM_YAML} \
    --stack-name ${SAM_STACK_NAME} \
    --capabilities CAPABILITY_IAM
