#!/bin/bash

#################

# Builds, tags, and pushes project container to ACR

#################

TAG=$(git rev-parse --short=7 HEAD)
sed "s/\[TAG\]/${TAG}/g" .k8s/prod/patch-deployment-project_copy.yaml > .k8s/prod/patch-deployment-project.yaml

IMAGE_PREFIX=$(az account list --all | jq '.[].user.name' | grep -i berkeley.edu | awk -F@ '{print $1}' | tr -d '"' | tr -d "." | tr '[:upper:]' '[:lower:]' | tr '_' '-' | uniq)

IMAGE_NAME=project
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"

az acr login --name w255mids

docker build --platform linux/amd64 -f ./mlapi/Dockerfile -t ${IMAGE_NAME}:${TAG} ./mlapi

docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_FQDN}:${TAG}
docker push ${IMAGE_FQDN}:${TAG}
docker pull ${IMAGE_FQDN}:${TAG}