#!/usr/bin/env bash

LAMBDAS=("searcher" "mail" "speech") # names of the directories which contain the lambdas
LAMBDA_FOLDER="lambda-zips/"
SAM_YAML="sam-infra.yaml" # sam-infra, under infra folder
SAM_STACK_NAME="twitter-searcher-stack" # default name for the stack, can be changed

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

if [ $# -lt 1 ]; then
    echo "Needs a bucket!"
    echo "Usage ./setup.sh <bucket>"
    exit 1
fi

BUCKET=$1

for folder in "${LAMBDAS[@]}"
do
    handle_lambda ${folder}
done

cd infra

echo "Deploying stack"
aws cloudformation deploy \
    --template-file ${SAM_YAML} \
    --stack-name ${SAM_STACK_NAME} \
    --capabilities CAPABILITY_IAM
