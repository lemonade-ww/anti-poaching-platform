#!/bin/bash

set -e

REGISTRY="pig208"
TAG=latest
CONTEXT=${PWD}
DOCKERFILE="Dockerfile"
PUSH=0
REMAINING_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--tag)
      TAG="$2"
      shift # past argument
      shift # past value
      ;;
    -c|--context)
      CONTEXT="$2"
      shift # past argument
      shift # past value
      ;;
    -f|--dockerfile)
      DOCKERFILE="$2"
      shift # past argument
      shift # past value
      ;;
    -T|--target)
      TARGET="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--push)
      PUSH=1
      shift
      ;;
    *)
      REMAINING_ARGS+=" $1"
      shift
      ;;
  esac
done

IMAGE_NAME=anti-poaching-${CONTEXT##*/}
TARGET=$(test "$TARGET" && echo "--target $TARGET" || :)

echo "${REGISTRY}/${IMAGE_NAME}:${TAG} -f $DOCKERFILE $TARGET $CONTEXT"

set -x

docker build -t ${REGISTRY}/${IMAGE_NAME}:${TAG} -f ${DOCKERFILE} $REMAINING_ARGS $CONTEXT
test PUSH = 1 && docker push ${REGISTRY}/${IMAGE_NAME}
