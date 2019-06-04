#!/bin/bash

IMAGE_NAME=rex2cidr

cd "$(dirname "$0")"
docker build -t "${IMAGE_NAME}" .
