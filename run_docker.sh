#!/bin/bash

IMAGE_NAME=rex2cidr

cd "$(dirname "$0")"
docker run -i "${IMAGE_NAME}" ./rex2cidr.py $*
