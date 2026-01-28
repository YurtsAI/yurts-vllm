#!/bin/bash

DOCKER_BUILDKIT=1 docker build \
  --platform linux/amd64 \
  --build-arg RUN_WHEEL_CHECK=false \
  --build-arg VLLM_USE_PRECOMPILED=true \
  --build-arg max_jobs=16 \
  --build-arg CUDA_VERSION=12.8.1 \
  --tag vllm-ci:build-image \
  --target build \
  --progress plain \
  -f docker/Dockerfile .

docker run --rm -v /home/jmob/dev/yurts-vllm/artifacts:/artifacts_host vllm-ci:build-image bash -c 'cp -r dist /artifacts_host && chmod -R a+rw /artifacts_host'
