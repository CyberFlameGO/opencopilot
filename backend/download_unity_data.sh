#!/bin/bash
ENV_DIR="."

# Load the .env file
if [ -f "${ENV_DIR}/.env" ]; then
    export $(grep -v '^#' "${ENV_DIR}/.env" | xargs)
else
    echo "No .env file found in directory: ${ENV_DIR}"
    exit 1
fi
COPILOT_UNITY_URL="https://storage.googleapis.com/docscloudstorage/2022.3/UnityDocumentation.zip"
case ${COPILOT_NAME} in
  "rpm")
    echo "Nothing to download, continue with ignesting data"
    exit 0
    ;;
  "unity")
    URL=$COPILOT_UNITY_URL
    FILE="UnityDocumentation.zip"
    ;;
  *)
    echo "Invalid COPILOT_NAME in .env file"
    exit 1
    ;;
esac

DIR="downloads"
if [ ! -d "$DIR" ]; then
  mkdir $DIR
fi
cd $DIR
curl -O $URL
unzip $FILE
rm $FILE
cd ..
echo "The documentation has been downloaded, continue with ignesting data"
