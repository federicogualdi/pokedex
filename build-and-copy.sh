#!/bin/bash

if [ $# -ne 3 ]; then
  echo -e "Please provide:\n\r\t-the aws profile\n\r\t-the aws ecr url\n\r\t-the docker tag"
  exit 0
fi

export AWS_PROFILE=$1
AWS_ECR_URL=$2
DOCKER_TAG=$3

IMAGE_VERSION=latest
DOCKER_CONTEXT=default
DATE=$( date "+%Y%m%d%H%M" )
DOCKER_FILE=src/main/docker/Dockerfile.jvm

docker context use ${DOCKER_CONTEXT}

./mvnw package -Dquarkus.container-image.build=true
docker build -f $DOCKER_FILE -t $DOCKER_TAG:$IMAGE_VERSION -t $DOCKER_TAG:$DATE .
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ECR_URL
docker tag $DOCKER_TAG:$IMAGE_VERSION $AWS_ECR_URL/$DOCKER_TAG:$IMAGE_VERSION
docker tag $DOCKER_TAG:$DATE $AWS_ECR_URL/$DOCKER_TAG:$DATE
docker push $AWS_ECR_URL/$DOCKER_TAG:$IMAGE_VERSION
docker push $AWS_ECR_URL/$DOCKER_TAG:$DATE