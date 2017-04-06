#!/usr/bin/env bash
set -e

docker build -t maciejpolanczyk/dbr-2 -f conf/python2/Dockerfile .
docker run maciejpolanczyk/dbr-2 python manage.py test

docker build -t maciejpolanczyk/dbr-3 -f conf/python3/Dockerfile .
docker run maciejpolanczyk/dbr-3 python3 manage.py test
